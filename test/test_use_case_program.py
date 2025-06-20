import datetime
import unittest

from src.data.data_source.data_source import MockProgramDataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository
from src.domain.program_day_use_case import ProgramDayUseCase
from src.presentation.view import MockDayView
from utils import mock_stdout


class DayUseCaseTest(unittest.TestCase):
    def setUp(self):
        data_source = MockProgramDataSource.from_file("mock/response_one_page.txt")
        repository = PHDRepository(parser=RSCParser(), data_source=data_source)
        self.use_case = ProgramDayUseCase(repository=repository, day=datetime.datetime.today())

    def test_present(self):
        view = MockDayView()
        self.use_case.add_view(view)
        with mock_stdout() as output:
            self.use_case.execute()
            self.assertEqual(output.getvalue().strip(), '500')
