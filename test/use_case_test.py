import unittest
from src.data.data_source.data_source import MockProgramDataSource
from src.data.parser.rsc_parser import RSCParser
from src.data.repository.repository import PHD2025Repository
from src.domain.use_case import ViewUseCase
from src.presentation.view import MockView
from utils import mock_stdout


class UseCaseTest(unittest.TestCase):
    def setUp(self):
        data_source = MockProgramDataSource.from_file("mock/one_page.txt")
        repository = PHD2025Repository(parser=RSCParser(), data_source=data_source)
        self.use_case = ViewUseCase(repository=repository)

    def test_add_view(self):
        view = MockView()
        self.assertEqual(self.use_case.count_view, 0)
        self.use_case.add_view(view)
        self.assertEqual(self.use_case.count_view, 1)

    def test_add_many_views(self):
        self.assertEqual(self.use_case.count_view, 0)
        views = [MockView() for _ in range(3)]
        self.use_case.add_views(views)
        self.assertEqual(self.use_case.count_view, len(views))

    def test_remove_view(self):
        view = MockView()
        self.assertEqual(self.use_case.count_view, 0)
        self.use_case.add_view(view)
        self.assertEqual(self.use_case.count_view, 1)
        self.use_case.remove_view(view)
        self.assertEqual(self.use_case.count_view, 0)

    def test_remove_not_last_view(self):
        self.assertEqual(self.use_case.count_view, 0)
        views = [MockView() for _ in range(3)]
        self.use_case.add_views(views)
        self.assertEqual(self.use_case.count_view, len(views))
        self.use_case.remove_view(views[0])
        self.assertEqual(self.use_case.count_view, len(views)-1)

    def test_remove_all_view(self):
        self.assertEqual(self.use_case.count_view, 0)
        views = [MockView() for _ in range(3)]
        self.use_case.add_views(views)
        self.assertEqual(self.use_case.count_view, len(views))
        self.use_case.remove_views(views)
        self.assertEqual(self.use_case.count_view, 0)

    def test_execute_view(self):
        view = MockView()
        self.use_case.add_view(view)
        with mock_stdout() as output:
            self.use_case.execute()
            self.assertEqual(output.getvalue().strip(), 'Hello world')

    def test_execute_many_view(self):
        views = [MockView() for _ in range(3)]
        self.use_case.add_views(views)
        with mock_stdout() as output:
            self.use_case.execute()
            self.assertEqual(
                output.getvalue().strip().split('\n'),
                ['Hello world', 'Hello world', 'Hello world']
            )

    def test_remove_single_not_existing_view(self):
        view = MockView()
        with self.assertRaises(ValueError):
            self.use_case.remove_view(view)

    def test_remove_not_existing_view(self):
        views = [MockView() for _ in range(3)]
        self.use_case.add_views(views)
        view = MockView()
        with self.assertRaises(ValueError):
            self.use_case.remove_view(view)
