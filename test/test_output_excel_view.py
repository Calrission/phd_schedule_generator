import datetime
import os.path
import unittest

from src.data.data_source.data_source import MockProgramDataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository
from src.domain.file_output_name_use_case import FileOutputNameUseCaseImpl, MockFileOutputNameUseCase
from src.domain.program_phd_use_case import PHDProgramUseCase
from src.presentation.excel_view import ExcelPHDProgramView


class TestOutputExcelView(unittest.TestCase):
    def setUp(self):
        self.mock_dir = "output"
        self.mock_base = "test"
        self.mock_file = f"{self.mock_base}.xlsx"

        if not os.path.exists(self.mock_dir):
            os.makedirs(self.mock_dir)

        repository = PHDRepository(
            parser=RSCParser(),
            data_source=MockProgramDataSource.from_file("mock/one_page.txt")
        )
        self.phd_program_use_case = PHDProgramUseCase(
            repository=repository,
            days=[datetime.date.today()]
        )
        file_output_use_case = MockFileOutputNameUseCase(
            base_output_filename=self.mock_base,
            mock_output_path=self.mock_dir
        )
        self.view = ExcelPHDProgramView(
            file_output_use_case=file_output_use_case
        )
        self.phd_program_use_case.add_view(self.view)

    def test_output_excel(self):
        self.phd_program_use_case.execute()
        self.assertTrue(os.path.exists(os.path.join(self.mock_dir, self.mock_file)))
