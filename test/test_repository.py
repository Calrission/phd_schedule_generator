import unittest
from datetime import datetime
from src.data.data_source.data_source import MockProgramDataSource
from src.data.models.report_model import ReportModel
from src.data.models.response_model import ResponseModel
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        parser = RSCParser()
        data_source = MockProgramDataSource.from_file("mock/response_one_page.txt")
        self.repo = PHDRepository(parser=parser, data_source=data_source)

    def test_fetch_one_page(self):
        response = self.repo.fetch_page(day=datetime.today(), page=1)
        self.assertTrue(isinstance(response, ResponseModel))
        self.assertTrue(len(response.placeholders) != 0)

    def test_fetch_all_page(self):
        response = self.repo.fetch_day(day=datetime.today())
        self.assertTrue(isinstance(response, list) and isinstance(response[0], ReportModel))
