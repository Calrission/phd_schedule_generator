import unittest

from src.core.config import Config


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.config = Config.from_file("../config.json")

    def test_config_test_all_filled(self):
        dict_config: dict = self.config.to_dict()
        values_config = list(dict_config.values())
        self.assertTrue(all([i is not None for i in values_config]))

    def test_config_all_filled(self):
        dict_config: dict = self.config.to_dict()
        values_config = list(dict_config.values())
        self.assertTrue(all([i is not None for i in values_config]))

    def test_key_raise_exception(self):
        with self.assertRaises(KeyError):
            _ = Config({})
