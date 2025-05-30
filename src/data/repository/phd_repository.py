import abc
import datetime
from json import loads
from typing import override

import loguru
from requests import RequestException

from src.data.data_source.data_source import DataSource
from src.data.models.error_model import ErrorModel
from src.data.models.report_model import ReportModel
from src.data.models.response_model import ResponseModel


class Repository(abc.ABC):
    @abc.abstractmethod
    def fetch_page(self, day: datetime.date, page: int) -> ResponseModel | ErrorModel: pass

    @abc.abstractmethod
    def fetch_day(self, day: datetime.date) -> list[ReportModel] | ErrorModel: pass


class PHDRepository(Repository):
    def __init__(self, parser, data_source: DataSource):
        self.parser = parser
        self.data_source = data_source

    @override
    def fetch_page(self, day: datetime.date, page: int) -> ResponseModel | ErrorModel:
        try:
            row_response: str = self.data_source.fetch(day, page)
            parsed_response: dict = self.parser.parse(row_response)
            # Always key 1 contains program data day
            response: dict = parsed_response.pop("1")
            return ResponseModel.from_dict(
                response,
                parsed_response
            )
        except RequestException as e:
            return ErrorModel(
                e.response.text
            )
        except Exception as e:
            return ErrorModel(
                "Unknown error"
            )

    @override
    def fetch_day(self, day: datetime.date) -> list[ReportModel] | ErrorModel:
        try:
            first_page = self.fetch_page(day, 1)
            reports = first_page.data
            for page_index in range(2, first_page.pagination.page_count + 1):
                loguru.logger.info(f"Fetching page {page_index}/{first_page.pagination.page_count}")
                page = self.fetch_page(day, page_index)
                reports.extend(page.data)
            return reports
        except RequestException as e:
            return ErrorModel(
                e.response.text
            )
        except Exception as e:
            return ErrorModel(
                "Unknown error"
            )


class MockRepository(Repository):
    def __init__(self, mock_response: ResponseModel | ErrorModel, mock_day: list[ReportModel] | ErrorModel):
        self.mock_response = mock_response
        self.mock_day = mock_day

    @staticmethod
    def from_day_file(day_file_path: str) -> 'MockRepository':
        with open(day_file_path, mode='r', encoding="utf-8") as day_file:
            return MockRepository(
                mock_day=[ReportModel.from_json(i) for i in loads(day_file.read())],
                mock_response=ErrorModel(
                    "This mock repository for only mock fetch_day. Use MockProgramDataSource to mock fetch_page."
                )
            )

    def fetch_page(self, day: datetime.date, page: int) -> ResponseModel | ErrorModel:
        return self.mock_response

    def fetch_day(self, day: datetime.date) -> list[ReportModel] | ErrorModel:
        return self.mock_day
