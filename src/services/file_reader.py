from interfaces.file_reader_interface import FileReader
from typing import List

class FixedWidthFileReader(FileReader):
    def read(self, file_path: str) -> List[str]:
        with open(file_path, 'r') as file:
            return file.readlines()
