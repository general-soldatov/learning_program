from .abstract import Parser, ParseXls, YamlCreator

class BookParser(Parser):
    def __init__(self, url):
        super().__init__(url)
        self.attr = {'name': 'pan', 'id': "doc-biblio-card"}

    def find_data(self, *args, **kwargs):
        return self._find_data().text.strip()

class MDParser(Parser):
    def __init__(self, url=None, path_md=None, test='ABCD'):
        super().__init__(url, path_md)
        self._rename(test)
        self.attr = {'name': 'h1'}

    def _rename(self, test):
        for i, item in enumerate(test, 1):
            self.page = self.page.replace(f'{item})', f'{i})')

    def find_data(self, *args, **kwargs):
        data = {
            key.text: {section.text: ''
                           for section in key.find_all_next('h2')}
                                for key in self._find_data(all_=True) if key.text
                                }
        # return self._soup.find(**self.attr).find_all_next('h2')
        return data

class ParseShedule(ParseXls):
    def search_code(self, code: str):
        self.max_row = 74
        self.row_index = self._search_to_column(code, col=2)
