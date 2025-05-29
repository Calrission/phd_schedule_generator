from datetime import datetime
import unittest

from src.core.config import Config
from src.data.data_source.phd_program_data_source import PHD2025DataSource


class DataSourceIntegrationTest(unittest.TestCase):
    def setUp(self):
        config = Config.from_file("../config.json")
        self.data_source = PHD2025DataSource(config.PHD_PROGRAM_URL)

    def test_fetch_first_page_not_empty(self):
        row_response: str = self.data_source.fetch(page=0, day=datetime.today())
        self.assertIsNotNone(row_response, "DataSource response is None")
        self.assertTrue(len(row_response) != 0, "DataSource response is empty")
