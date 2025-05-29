import json

from src.core.datetime_utils import str2date


class Config:
    PHD_PROGRAM_URL = None
    DAYS = None
    BASE_OUTPUT_FILENAME = None

    @staticmethod
    def __safe_get(config: dict, key: str):
        value = config.get(key)
        if value is None:
            raise KeyError(f'"{key}" is missing')
        return value

    def __init__(self, config_json: dict) -> None:
        self.PHD_PROGRAM_URL = self.__safe_get(config_json, 'PHD_PROGRAM_URL')
        self.DAYS = [str2date(i) for i in self.__safe_get(config_json, 'DAYS')]
        self.BASE_OUTPUT_FILENAME = self.__safe_get(config_json, 'BASE_OUTPUT_FILENAME')

    @staticmethod
    def from_str(config_str: str) -> 'Config':
        return Config(json.loads(config_str))

    @staticmethod
    def from_file(path: str) -> 'Config':
        with open(path, 'r') as f:
            return Config(json.load(f))

    def to_dict(self):
        return self.__dict__
