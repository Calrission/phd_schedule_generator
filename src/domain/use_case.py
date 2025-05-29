from src.data.repository.phd_repository import PHDRepository


class ViewUseCase:
    def __init__(self, repository: PHDRepository):
        self._repository = repository
        self._views = []

    @property
    def count_view(self):
        return len(self._views)

    def _prepare_view(self, view):
        pass

    def _idle(self):
        pass

    def _prepare(self):
        self._idle()
        for view in self._views:
            self._prepare_view(view)

    def execute(self):
        self._prepare()
        for view in self._views:
            view.present()

    def add_view(self, view):
        self._views.append(view)

    def remove_view(self, view):
        self._views.remove(view)

    def add_views(self, views):
        self._views.extend(views)

    def remove_views(self, views):
        for view in views:
            self.remove_view(view)
