from .abstract import WordDocument
from .parser import ParseShedule, BookParser
from .config import Themes, Literatures, Program

class WorkPlan(WordDocument):
    def __init__(self, data, path_doc = None, path = "", _bar_max=10):
        super().__init__(data, path_doc, path, _bar_max=_bar_max)
        self.type_doc = 'РП'


    @staticmethod
    def roman_digit(num: int):
        semesters = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        return semesters[num]

    @staticmethod
    def volume_create(volume_last: dict) -> list:
        volume = []
        for semester, value in volume_last.items():
            data_volume = {'semester': WorkPlan.roman_digit(semester)}
            data_volume.update(value)
            data_volume['contact'] = data_volume['Лек'] + data_volume['Лаб'] + data_volume['Пр']
            volume.append(data_volume)

        if len(volume) < 2:
            volume.append({key: 0 for key, _ in volume[0]})

        data = {}
        for elem in volume:
            for key, value in elem.items():
                data.setdefault(key, 0)
                if isinstance(value, int):
                    data[key] += value

        volume.append(data)
        return volume

    @staticmethod
    def get_liter(liter: Literatures):
        context = {'basic': [], 'optional': []}
        for key in context.keys():
            for elem in liter.__dict__[key]:
                book = BookParser(elem)
                context[key].append(book.find_data())
        return context

    @staticmethod
    def themes_plan(volume_last: dict, themes: list, division: int):
        keys = tuple(volume_last.keys())
        if len(keys) == 2:
            themes_ = [themes[:division], themes[division:]]
            volume_last[keys[0]]['themes'] = {i+1: themes_[0][i] for i in range(division)}
            volume_last[keys[1]]['themes'] = {i+1: themes_[1][i-division] for i in range(division, len(themes))}
            return volume_last

        volume_last[keys[0]]['themes'] = {i: themes[i] for i in range(1, len(themes)+1)}
        return volume_last

    @staticmethod
    def parse_competition(shedule: ParseShedule) -> dict:
        context = {}
        shedule.search_competition()
        context['competition'] = shedule.abstract_of_competition
        context['name'] = shedule.name
        return context

    def parse_semester(self, shedule: ParseShedule) -> dict:
        shedule.search_semester()
        self.volume_last = shedule.data_course
        self.context.update(self.parse_competition(shedule))
        self.bar.next()

    def create_app_fund(self, program: Program):
        self.context['tasks_type'] = program.type_
        self.context['benchmark'] = {key: program.competition[i] for i, key
                                     in enumerate(self.context['competition'].keys())}
        self.context['num_comp'] = ','.join(self.context['competition'].keys())
        self.context['control'] = ', '.join(item['Формы контр.'] for _, item in self.volume_last.items())
        self.bar.next()


    def create_plan(self, themes: Themes, program: Program, liter: Literatures):
        self.context['themes_plan'] = self.themes_plan(self.volume_last, themes.list_of, themes.semester_division)
        self.context['place_last'] = ', '.join(map(lambda x: f"«{x}»", program.place_of_learning['last']))
        self.context['place_future'] = ', '.join(map(lambda x: f"«{x}»", program.place_of_learning['future']))
        self.context['volume'] = self.volume_create(self.volume_last)
        self.bar.next()
        self.context['liter'] = self.get_liter(liter)
        self.context['hours'] = self.context['volume'][2]['Итого']
        self.context['zet'] = int(self.context['hours'] / 36)
        self.bar.next()

    def add_with_project(self, themes: Themes, liter: Literatures, program: Program, shedule: ParseShedule):
        context = {'themes': themes.list_of}
        self.bar.next()
        self.context.update(context)
        self.bar.next()
        self.parse_semester(shedule)
        self.create_app_fund(program)
        self.create_plan(themes, program, liter)


class AppraisalFunds(WorkPlan):
    def __init__(self, data, path_doc=None, path=""):
        super().__init__(data, path_doc, path, _bar_max=6)
        self.type_doc = "ФОС"

    def add_with_project(self, program, shedule):
        self.parse_semester(shedule)
        self.create_app_fund(program)
