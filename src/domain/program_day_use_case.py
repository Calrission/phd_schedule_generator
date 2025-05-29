from datetime import datetime
from typing import override
import loguru
from src.data.models.error_model import ErrorModel
from src.data.repository.phd_repository import PHDRepository
from src.domain.use_case import ViewUseCase
from src.presentation.view import ProgramDayView


class ProgramDayUseCase(ViewUseCase):
    def __init__(self, repository: PHDRepository, day: datetime.date):
        super().__init__(repository)
        self._program = None
        self._day = day

    @override
    def add_view(self, view: ProgramDayView):
        if not isinstance(view, ProgramDayView):
            raise TypeError
        super().add_view(view)

    @override
    def _prepare_view(self, view: ProgramDayView):
        view.set_program(self._program)

    @override
    def _idle(self):
        data = self._repository.fetch_day(self._day)
        match type(data):
            case ErrorModel():
                loguru.logger.exception(data.error)
            case _:
                self._program = data
