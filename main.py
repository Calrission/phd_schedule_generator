from src.core.config import Config
from src.data.data_source.phd_program_data_source import PHD2025DataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.phd_repository import PHDRepository
from src.domain.file_output_name_use_case import FileOutputNameUseCaseImpl
from src.domain.program_phd_use_case import PHDProgramUseCase
from src.presentation.excel_view import ExcelPHDProgramView
from src.presentation.json_view import JsonView

config = Config.from_file("config.json")
program_data_source = PHD2025DataSource(
    phd_program_url=config.PHD_PROGRAM_URL
)
rsc_parser = RSCParser()
repository = PHDRepository(
    parser=rsc_parser,
    data_source=program_data_source
)
phd_program_use_case = PHDProgramUseCase(
    repository=repository,
    days=config.DAYS
)
file_output_use_case = FileOutputNameUseCaseImpl(
    base_output_filename=config.BASE_OUTPUT_FILENAME
)
excel_view = ExcelPHDProgramView(
    file_output_use_case=file_output_use_case
)
json_view = JsonView(
    file_output_use_case=file_output_use_case,
)
phd_program_use_case.add_view(excel_view)
phd_program_use_case.add_view(json_view)
phd_program_use_case.execute()
