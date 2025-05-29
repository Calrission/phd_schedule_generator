import abc
import os
from datetime import datetime
from os.path import join
from typing import override


class FileOutputNameUseCase(abc.ABC):
    def __init__(self, base_output_filename: str):
        self.base_output_filename = base_output_filename

    @abc.abstractmethod
    def get_available_output_name(self, format_file: str):
        pass


class FileOutputNameUseCaseImpl(FileOutputNameUseCase):
    def __init__(self, base_output_filename: str):
        super(FileOutputNameUseCaseImpl, self).__init__(base_output_filename)

    @override
    def get_available_output_name(self, format_file: str):
        os.makedirs("output", exist_ok=True)
        new_name = f"{self.base_output_filename}_{datetime.today().timestamp()}.{format_file}"
        return join("output", new_name)
