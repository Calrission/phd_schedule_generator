from datetime import datetime
from typing import override

import loguru

from src.core.datetime_utils import date2str
from src.data.models.error_model import ErrorModel
from src.data.repository.phd_repository import Repository
from src.domain.use_case import ViewUseCase
from src.presentation.view import PHDProgramView


class PHDProgramUseCase(ViewUseCase):
    def __init__(self, repository: Repository, days: list[datetime.date]):
        super().__init__(repository)
        self._phd_program = None
        self._days = days

    @override
    def _idle(self):
        self._phd_program = {}
        for day in self._days:
            loguru.logger.info(f"DAY - {date2str(day)}")
            data = self._repository.fetch_day(day)
            self._phd_program[day] = []
            match type(data):
                case ErrorModel():
                    loguru.logger.exception(data.error)
                case _:
                    self._phd_program[day] = data

    @override
    def _prepare_view(self, view: PHDProgramView):
        view.set_phd_program(self._phd_program)
