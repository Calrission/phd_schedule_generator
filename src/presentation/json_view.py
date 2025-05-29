import json
from loguru import logger

from src.core.datetime_utils import date2str
from src.domain.file_output_name_use_case import FileOutputNameUseCase
from src.presentation.view import PHDProgramView


class JsonView(PHDProgramView):
    def __init__(self, file_output_use_case: FileOutputNameUseCase):
        super().__init__()
        self.__file_output_use_case = file_output_use_case

    def present(self):
        logger.info("Executing JsonView")
        json_file_name = self.__file_output_use_case.get_available_output_name(format_file="json")
        data = {}
        for i, e in self._phd_program.items():
            key_str = date2str(i)
            value_list_dict = [j.to_json() for j in e]
            data[key_str] = value_list_dict
        with open(json_file_name, "x", encoding="utf-8") as json_file:
            json_file.write(json.dumps(data, ensure_ascii=False).encode("utf-8").decode())
        logger.info(f"Finish execute JsonView - {json_file_name}")
