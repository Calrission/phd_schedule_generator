from datetime import datetime
from typing import override

from src.data.models.error_model import ErrorModel
from src.data.repository.repository import PHD2025Repository
from src.domain.use_case import ViewUseCase
from src.presentation.view import PageView


class OnePageUseCase(ViewUseCase):
    def __init__(self, repository: PHD2025Repository, day: datetime.date, page: int = 1):
        super().__init__(repository)
        self.day = day
        self.page = page
        self.response = None

    @override
    def add_view(self, view: PageView):
        if not isinstance(view, PageView):
            raise TypeError
        super().add_view(view)

    @override
    def _prepare_view(self, view):
        view.set_page(self.response)

    @override
    def _idle(self):
        data = self._repository.fetch_page(self.day, self.page)
        match type(data):
            case ErrorModel():
                raise Exception(data.error)
            case _:
                self.response = data
