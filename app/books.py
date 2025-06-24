from .abstract import Parser, ParseXls, YamlCreator

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

    @staticmethod
    def num_semester(course: str, session: str) -> int:
        sessions = {
            'Летняя сессия': 0,
            'Зимняя сессия': -1
        }
        return 2 * int(course[-1]) + sessions[session]

    @staticmethod
    def roman_digit(num: int):
        semesters = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        return semesters[num]

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
