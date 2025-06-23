from .abstract import Parser

class BookParser(Parser):
    def __init__(self, url):
        super().__init__(url)

    def find_data(self, *args, **kwargs):
        return self._find_data().text.strip()

class MDParser(Parser):
    def __init__(self, url=None, path_md=None):
        super().__init__(url, path_md)
        self._rename()

    def _rename(self):
        for i, item in enumerate('ABCD', 1):
            self.page = self.page.replace(f'{item})', f'{i})')

    def find_data(self, *args, **kwargs):
        return self.page
