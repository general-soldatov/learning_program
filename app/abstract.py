import openpyxl
import requests
import yaml
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class Parser(ABC):
    def __init__(self, url=None):
        self.__get_url(url)
        self.parser = "html.parser"
        self.attr = {}

    def __get_url(self, url):
        if url:
            self.url = url
            self.page = requests.get(self.url).text

    def _find_data(self, all_=False, **kwargs) -> list | str:
        self._soup = BeautifulSoup(self.page, self.parser)
        if not all_:
            return self._soup.find(**self.attr, **kwargs)
        return self._soup.find_all(**self.attr, **kwargs)

    @abstractmethod
    def find_data(self, *args, **kwargs):
        pass

class ParseXls:
    def __init__(self, path, name=None, max_RC: bool|tuple =False):
        self.workbook = openpyxl.load_workbook(path, read_only=True)
        self._worksheet(name)
        self.row_index = None
        if self.sheet.max_row and not max_RC:
            self.max_row = self.sheet.max_row
            self.max_col = self.sheet.max_column
        self.max_row, self.max_col = max_RC

    def _worksheet(self, name):
        self.sheet = self.workbook.active
        if name:
            self.sheet = self.workbook[name]

    def _search_to_column(self, to_scan: str, col: int, start: int = 1) -> int:
        for row in range(start, self.max_row + 1):
            if self.sheet.cell(row, col).value == to_scan:
                return row

    @staticmethod
    def _search_with_column(sheet, to_scan: str, col: int, start: int = 1, stop: int = 1) -> int:
        for row in range(start, stop + 1):
            if sheet.cell(row, col).value == to_scan:
                return row


class YamlCreator:
    def __init__(self, path: str, encoding: str = 'utf-8'):
        self._path = path
        with open(path, 'r', encoding=encoding) as project:
            self._data = yaml.safe_load(project)

    def recording(self, path: str = None, encoding: str = 'utf-8'):
        if not path:
            path = self._path
        with open(path, 'w', encoding=encoding) as project:
            yaml.dump(self._data, project)