from .abstract import Parser, ParseXls, YamlCreator
from .config import Paths, Program, Themes, Literatures

class ProjectReader(YamlCreator):
    def __init__(self, path, encoding = 'utf-8'):
        super().__init__(path, encoding)
        self.import_paths()

    def import_paths(self):
        self.paths: Paths = Paths(**self._data['path'])
        self.program: Program = Program(**self._data['program'])

    def import_data(self):
        self.themes: Themes = Themes(**self._data['themes'])
        self.literatures: Literatures = Literatures(**self._data['literatures'])


class BookParser(Parser):
    def __init__(self, url):
        super().__init__(url)
        self.attr = {'name': 'pan', 'id': "doc-biblio-card"}

    def find_data(self, *args, **kwargs):
        return self._find_data().text.strip()

# class MDParser(Parser):
#     def __init__(self, url=None, path_md=None, test='ABCD'):
#         super().__init__(url, path_md)
#         self._rename(test)
#         self.attr = {'name': 'h1'}

#     def _rename(self, test):
#         for i, item in enumerate(test, 1):
#             self.page = self.page.replace(f'{item})', f'{i})')

#     def find_data(self, *args, **kwargs):
#         data = {
#             key.text: {section.text: ''
#                            for section in key.find_all_next('h2')}
#                                 for key in self._find_data(all_=True) if key.text
#                                 }
#         return data

class ParseShedule(ParseXls):
    def __init__(self, path, name=None, max_RC = (74, 103)):
        super().__init__(path, name, max_RC)


    def search_code(self, code: str):
        self.row_index = self._search_to_column(code, col=2)
        self.name = self.sheet.cell(self.row_index, column=3).value

    @staticmethod
    def num_semester(course: str, session: str) -> int:
        sessions = {
            'Летняя сессия': 0,
            'Зимняя сессия': -1
        }
        return 2 * int(course[-1]) + sessions[session]

    @staticmethod
    def type_control(data: dict) -> None:
        control = {
            'з': 'Зачёт',
            'э': 'Экзамен'
        }
        data['Формы контр.'] = control.get(data['Формы контр.'], 'Экзамен')

    @staticmethod
    def correct_data(data: dict) -> dict:
        data_course = {}
        for key, value in data.items():
            if value is None:
                data_course[key] = 0
            elif value.isdigit():
                data_course[key] = int(value)
            else:
                data_course[key] = value
        return data_course

    @staticmethod
    def group_competition(text: str) -> list:
        grouped_codes = {}
        for code in text.split(sep='; '):
            sp_code = code.split('-')
            key = f"{sp_code[0]}-{sp_code[1].split(sep='.')[0]}"
            grouped_codes.setdefault(key, [])
            grouped_codes[key].append(code)
        return grouped_codes

    def _decode_competition(self, rows=1):
        self.abstract_of_competition = {}
        competition_sheet = self.workbook['Компетенции']
        for comp_key, comp_list in self.competition.items():
            row_comp = self._search_with_column(competition_sheet, comp_key, col=1, stop=rows)
            self.abstract_of_competition.setdefault(comp_key,
                                               {'text': competition_sheet.cell(row_comp, 4).value,
                                               'data': {}})
            for elem in comp_list:
                row_elem = self._search_with_column(competition_sheet, elem, col=2, start=row_comp, stop=rows)
                self.abstract_of_competition[comp_key]['data'][elem] = competition_sheet.cell(row_elem, 4).value


    def search_semester(self):
        self.data_course = {}
        for course in range(16, 101, 17):
            for semester in range(course + 1, course + 16, 8):
                if (self.sheet.cell(self.row_index, semester).value):
                    data = {
                            self.sheet.cell(3, i).value: self.sheet.cell(self.row_index, i).value
                            for i in range(semester, semester + 8)
                        }
                    self.type_control(data)
                    num_of_sem = self.num_semester(self.sheet.cell(1, course).value,
                                                   self.sheet.cell(2, semester).value)
                    self.data_course[num_of_sem] = self.correct_data(data)

    def search_competition(self):
        column_competition = 103
        text = self.sheet.cell(self.row_index, column_competition).value
        self.competition: dict = self.group_competition(text)
        self._decode_competition(rows=583)
