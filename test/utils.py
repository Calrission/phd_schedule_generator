from io import StringIO
from unittest.mock import patch


def mock_stdout():
    return patch('sys.stdout', new=StringIO())
