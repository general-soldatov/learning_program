from .abstract import WordDocument
from .parser import ParseShedule

class WorkPlan(WordDocument):
    def __init__(self, data, path_doc = None, path = ""):
        super().__init__(data, path_doc, path)
        self.type_doc = 'РП'

    def create_learn_time(self, shedule: ParseShedule):
        shedule.search_semester()
        self.context['']
        shedule.data_course # расчасовка по семестрам

    def add_with_project(self, *args):
        pass
