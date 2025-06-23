import markdown
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class Parser(ABC):
    def __init__(self, url=None, path_md=None):
        self.__get_url(url)
        self.__get_markdown(path_md)
        self.parser = "html.parser"
        self.attr = {'name': 'pan', 'id': "doc-biblio-card"}

    def __get_url(self, url):
        if url:
            self.url = url
            self.page = requests.get(self.url)

    def __get_markdown(self, path):
        if path:
            with open(path, 'r', encoding='utf-8') as input_data:
                input_text = input_data.read()
                self.page = markdown.markdown(input_text)

    def _find_data(self):
        soup = BeautifulSoup(self.page.text, self.parser)
        return soup.find(**self.attr)

    @abstractmethod
    def find_data(self, *args, **kwargs):
        pass
