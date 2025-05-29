import unittest
from src.data.parser.rsc_parser import RSCParser


class RSCParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = RSCParser()
        with open("mock/one_page.txt", "r", encoding="utf-8") as f:
            self.mock_day_page = f.read()

    def test_simple_parse(self):
        text = "1:Hello world"
        result = self.parser.parse(text)
        self.assertEqual(result["1"], "Hello world")

    def test_multiline_value_parse(self):
        text = "1:Hello world\nHello PHD"
        result = self.parser.parse(text)
        self.assertEqual(result["1"], "Hello world\nHello PHD")

    def test_multikey_simple_parse(self):
        text = "1:Hello world\n2:Hello PHD"
        result = self.parser.parse(text)
        self.assertEqual(result["1"], "Hello world")
        self.assertEqual(result["2"], "Hello PHD")

    def test_multikey_multiline_value_parse(self):
        text = "1:Hello\nworld\n2:Hello\nPHD"
        result = self.parser.parse(text)
        self.assertEqual(result["1"], "Hello\nworld")
        self.assertEqual(result["2"], "Hello\nPHD")

    def test_json_parse(self):
        text = '1:{"test":"test"}'
        result = self.parser.parse(text)
        self.assertEqual(result["1"], {"test": "test"})

    def test_placeholder_json_parse(self):
        text = '1:{"test":"$2"}\n2:test'
        result = self.parser.parse(text)
        self.assertEqual(result["1"], {"test": "test"})

    def test_time_parse(self):
        text = '1:TIME - 18:00\n2:TIME - 19:00'
        result = self.parser.parse(text)
        keys = list(result.keys())
        self.assertNotIn("8", keys)
        self.assertNotIn("9", keys)

    def test_merged_key_parse(self):
        text = '1:Hello PHD!2:Hello World!'
        result = self.parser.parse(text)
        keys = list(result.keys())
        self.assertIn("1", keys)
        self.assertIn("2", keys)

    def test_json_data_mock_day_page(self):
        result = self.parser.parse(self.mock_day_page)
        self.assertTrue(isinstance(result["1"], dict))
