import abc
from typing import override

from src.core.alias import ProgramDay, ProgramPHD
from src.data.models.response_model import ResponseModel


class View(abc.ABC):
    @abc.abstractmethod
    def present(self):
        raise NotImplementedError


class PageView(View, abc.ABC):
    def __init__(self):
        self._page: ResponseModel | None = None

    def set_page(self, page):
        self._page = page


class ProgramDayView(View, abc.ABC):
    def __init__(self):
        self._program_day: ProgramDay | None = None

    def set_program(self, program: ProgramDay):
        self._program_day = program


class PHDProgramView(View, abc.ABC):
    def __init__(self):
        self._phd_program: ProgramPHD | None = None

    def set_phd_program(self, program: ProgramPHD):
        self._phd_program = program


class MockView(View):
    @override
    def present(self):
        print("Hello world")


class MockPageView(PageView):
    def present(self):
        print(self._page.pagination)


class MockDayView(ProgramDayView):
    def present(self):
        print(len(self._program_day))


class MockPHDProgramView(PHDProgramView):
    def present(self):
        amount = sum([len(i) for i in self._phd_program.values()])
        print(amount)
