from bs4 import BeautifulSoup
import requests
from app.abstract import create_division

from app.parser import BookParser, ProjectReader, ParseShedule
from app.word_template import WorkPlan, AppraisalFunds, Metodical

data_prog = {
    'start': 'start program'.upper(),
    'end': 'end program'.upper()
}
print(create_division(data_prog['start']))
data_yaml = ProjectReader('projects/databases.yaml')
print('Open Exel File')
shedule = ParseShedule(data_yaml.paths.shedule, name='План')
shedule.search_code(data_yaml.program.code)
data_yaml.import_data()

def part_one():
    shedule.search_competition()
    print("Selected competition:")
    print(shedule.abstract_of_competition)

def part_two():
    # print("Create document: Work Plan")
    # wp = WorkPlan(data_yaml.program, path_doc=data_yaml.paths.work_program, path=data_yaml.paths.folder)
    # wp.add_with_project(data_yaml.themes, data_yaml.literatures, data_yaml.program, shedule)
    # print(wp.create_document())
    # print("Create document: Appraisal Funds")
    # af = AppraisalFunds(data_yaml.program, path_doc=data_yaml.paths.appraisal_funds, path=data_yaml.paths.folder)
    # af.add_with_project(data_yaml.program, shedule)
    # print(af.create_document())
    print("Create document: Metodical")
    mw = Metodical(data_yaml.program, path_doc=data_yaml.paths.metodical, path=data_yaml.paths.folder)
    mw.add_with_project(data_yaml.themes, data_yaml.literatures, data_yaml.program, shedule)
    print(mw.create_document())

if __name__ == '__main__':
    # part_one()
    part_two()
    print(create_division(data_prog['end']))
    # print(data_yaml.literatures.basic[0]+'#bib')
    # print(BookParser(data_yaml.literatures.basic[0]).find_data())