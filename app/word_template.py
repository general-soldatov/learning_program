from .abstract import WordDocument
from .parser import ParseShedule
from .config import Themes, Literatures

class WorkPlan(WordDocument):
    def __init__(self, data, path_doc = None, path = ""):
        super().__init__(data, path_doc, path)
        self.type_doc = 'РП'


    @staticmethod
    def roman_digit(num: int):
        semesters = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        return semesters[num]

    def create_learn_time(self, shedule: ParseShedule):
        shedule.search_semester()
        self.context['']
        shedule.data_course # расчасовка по семестрам

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
    def themes_plan(volume_last: dict, themes: list, division: int):
        keys = tuple(volume_last.keys())
        if len(keys) == 2:
            themes_ = [themes[:division], themes[division:]]
            volume_last[keys[0]]['themes'] = {i+1: themes_[0][i] for i in range(division)}
            volume_last[keys[1]]['themes'] = {i+1: themes_[1][i-division] for i in range(division, len(themes))}
            return volume_last

        volume_last[keys[0]]['themes'] = {i: themes[i] for i in range(1, len(themes)+1)}
        return volume_last

    def add_with_project(self, themes: Themes, liter: Literatures):
        context = {
            'place_last': "«Базы данных», «Операционные системы», «Основы программирования и алгоритмизации», «Технологии тестирования информационных систем», «Автоматизация проектирования информационных систем»",
            'place_future': "«Web-программирование в информационных системах», «Автоматизация проектирования информационных систем» и других",
            'hours': 288,
            'competition': {'ПК-2': {'text': 'Способен выполнять работы по созданию (модификации) и сопровождению информационных систем и ресурсов для различных прикладных областей', 'data': {'ПК-2.1': 'Демонстрирует знания устройств и функционирования современных ИС, возможностей типовых ИС, методов моделирования бизнес-процессов в ИС.', 'ПК-2.2': 'Способен тестировать ИС и ее модули, устанавливать необходимое программное обеспечение, устанавливать и настраивать оборудование. ', 'ПК-2.3': 'Владеет навыками определения необходимых изменений в ИС, оценки влияния изменений на функциональные и нефункциональные характеристики ИС.'}}},
            'themes': themes.list_of
        }
        volume_last = {7: {'Итого': 108, 'Лек': 4, 'Лаб': 0, 'Пр': 6, 'Конс': 0, 'СР': 94, 'Конт роль': 4, 'Формы контр.': 'Зачёт'}, 8: {'Итого': 180, 'Лек': 8, 'Лаб': 0, 'Пр': 10, 'Конс': 0, 'СР': 153, 'Конт роль': 9, 'Формы контр.': 'Экзамен'}}

        context['themes_plan'] = self.themes_plan(volume_last, themes.list_of, themes.semester_division)
        context['volume'] = self.volume_create(volume_last)
        context['zet'] = int(context['hours'] / 36)
        self.context.update(context)
