import datetime
import unittest

from src.data.data_source.data_source import MockProgramDataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository
from src.domain.program_phd_use_case import PHDProgramUseCase
from src.presentation.view import MockPHDProgramView
from utils import mock_stdout


class ProgramPhdUseCaseTest(unittest.TestCase):
    def setUp(self):
        data_source = MockProgramDataSource.from_file("mock/one_page.txt")
        repository = PHDRepository(parser=RSCParser(), data_source=data_source)
        self.use_case = PHDProgramUseCase(
            repository,
            days=[
                datetime.date(2025, 5, 22),
                datetime.date(2025, 5, 23),
                datetime.date(2025, 5, 24),
            ]
        )

    def test_present(self):
        view = MockPHDProgramView()
        self.use_case.add_view(view)
        with mock_stdout() as output:
            self.use_case.execute()
            self.assertEqual(output.getvalue().strip(), '1500')
