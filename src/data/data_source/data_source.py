import abc
import datetime


class DataSource(abc.ABC):
    def fetch(self, day: datetime.date, page: int) -> str:
        raise NotImplementedError


class MockProgramDataSource(DataSource):
    def __init__(self, mock_data: str) -> None:
        self._mock_data = mock_data

    @staticmethod
    def from_file(path: str) -> DataSource:
        with open(path, 'r', encoding="utf-8") as f:
            return MockProgramDataSource(f.read())

    def fetch(self, day: datetime.date, page: int) -> str:
        return self._mock_data
