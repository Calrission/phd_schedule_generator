import datetime
import enum
from typing import override

from loguru import logger
from openpyxl.styles import Alignment, Font
from openpyxl.workbook import Workbook

from src.core.alias import ProgramDay, ProgramPHD
from src.domain.file_output_name_use_case import FileOutputNameUseCase
from src.presentation.view import PHDProgramView

HEIGHT_HEADER = 4


class Column(enum.Enum):
    time = "A"
    name = "B"
    tag = "C"
    talk_type = "D"
    place = "E"
    description = "F"
    speakers = "G"
    short = "H"
    broadcast = "I"

    @staticmethod
    def first() -> 'Column':
        return [*Column][0]

    @staticmethod
    def last() -> 'Column':
        return [*Column][-1]

    @staticmethod
    def count() -> int:
        return len(Column)

    def __str__(self):
        return self.value


class ExcelPHDProgramView(PHDProgramView):
    def __init__(self, file_output_use_case: FileOutputNameUseCase):
        super().__init__()
        self.__file_output_name_use_case = file_output_use_case
        self._wb = Workbook()

    @property
    def __page(self):
        return self._wb.active

    @override
    def present(self):
        logger.info("Presenting Excel View")
        for i, (day, program_day) in enumerate(self._phd_program.items()):
            self.__page.title = day.strftime("%d.%m.%Y")
            self.__tune_header_cells()
            self.__fill_page_day(day, program_day)
            if i != len(self._phd_program) - 1:
                self.__create_new_list()
        self.__save()

    def __save(self):
        name = self.__file_output_name_use_case.get_available_output_name(format_file="xlsx")
        logger.info(f"Saving Excel View with {name=}")
        self._wb.save(name)

    def __create_new_list(self):
        ws = self._wb.create_sheet()
        self._wb.active = self._wb.worksheets.index(ws)

    def __fill_page_day(self, day: datetime.date, program_day: ProgramDay):
        self.__fill_header(day)
        self.__fill_content(program_day)

    def __tune_header_cells(self):
        for column in self.__page.iter_rows(min_col=1, max_col=Column.count(), min_row=1, max_row=HEIGHT_HEADER-1):
            for cell in column:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.font = Font(bold=True)

    def __fill_content(self, program_day: ProgramDay):
        def fill_column(letter: str, index: int, value: str, is_center: bool = True):
            cell = self.__page[f'{letter}{index}']
            cell.value = value
            if is_center:
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            else:
                cell.alignment = Alignment(wrap_text=True, vertical='center')

        for i in range(len(program_day)):
            e = program_day[i]
            row = i + HEIGHT_HEADER
            fill_column(Column.time.value, row, e.time)
            fill_column(Column.tag.value, row, e.tag.name)
            fill_column(Column.name.value, row, e.title)
            fill_column(Column.place.value, row, e.map_object.title)
            fill_column(Column.speakers.value, row, ", ".join([f"{i.name} ({i.company})" for i in e.speakers]))
            fill_column(Column.description.value, row, e.description if e.description is not None else "-", False)
            fill_column(Column.talk_type.value, row, e.talk_type.name if e.talk_type is not None else "-")
            fill_column(Column.broadcast.value, row, "Есть" if e.is_visible_in_broadcast else "Нету")
            fill_column(Column.short.value, row, f"{e.time}\n{e.title}\n{e.map_object.title}")

    def __fill_header(self, day: datetime.date):
        self.__page['A1'] = f"СОЗДАН {datetime.datetime.today().strftime('%d.%m.%Y')}"
        self.__page['B1'] = day.strftime('PHD - %d.%m.%Y')
        self.__page.merge_cells(f'{Column.first()}1:{Column.last()}1')

        def fill_header_column(column_latter: str, title: str, width: int | None):
            self.__page[f'{column_latter}2'] = title
            self.__page.merge_cells(f'{column_latter}2:{column_latter}3')
            if width is not None:
                self.__page.column_dimensions[column_latter].width = width

        fill_header_column(Column.time.value, "Время", 13)
        fill_header_column(Column.name.value, "Наименование", 80)
        fill_header_column(Column.tag.value, "Трек", 30)
        fill_header_column(Column.talk_type.value, "Тип", 25)
        fill_header_column(Column.place.value, "Зал", 25)
        fill_header_column(Column.speakers.value, "Спикеры", 40)
        fill_header_column(Column.description.value, "Описание", 100)
        fill_header_column(Column.short.value, "SHORT", 40)
        fill_header_column(Column.broadcast.value, "Трансляция", 15)
