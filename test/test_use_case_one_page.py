import unittest
from datetime import datetime

from src.data.data_source.data_source import MockProgramDataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository
from src.domain.one_page_use_case import OnePageUseCase
from src.presentation.view import MockView, MockPageView
from utils import mock_stdout


class OnePageUseCaseTest(unittest.TestCase):
    def setUp(self):
        data_source = MockProgramDataSource.from_file("mock/one_page.txt")
        repository = PHDRepository(parser=RSCParser(), data_source=data_source)
        self.use_case = OnePageUseCase(repository=repository, day=datetime.today())

    def test_present(self):
        view = MockPageView()
        self.use_case.add_view(view)
        with mock_stdout() as output:
            self.use_case.execute()
            self.assertEqual(output.getvalue().strip(), "page=3 pageSize=10 pageCount=50 total=500")

    def test_raise_add_not_page_view(self):
        view = MockView()
        with self.assertRaises(TypeError):
            self.use_case.add_view(view)
            