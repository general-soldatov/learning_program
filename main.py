from bs4 import BeautifulSoup
import requests
import os

from app.parser import BookParser, ProjectReader, ParseShedule
from app.word_template import WorkPlan

data_yaml = ProjectReader('projects/databases.yaml')
shedule = ParseShedule(data_yaml.paths.shedule, name='План')
shedule.search_code(data_yaml.program.code)
data_yaml.import_data()
data_yaml.program.name = shedule.name

def part_one():
    shedule.search_competition()
    print(shedule.abstract_of_competition)

def part_two():
    wp = WorkPlan(data_yaml.program, path_doc=data_yaml.paths.work_program, path=data_yaml.paths.folder)
    wp.add_with_project(data_yaml.themes, data_yaml.literatures, data_yaml.program, shedule)
    print(wp.create_document())

if __name__ == '__main__':
    # part_one()
    part_two()
    # print(data_yaml.literatures.basic[0]+'#bib')
    # print(BookParser(data_yaml.literatures.basic[0]).find_data())