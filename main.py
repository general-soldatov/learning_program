from bs4 import BeautifulSoup
import requests

# url = "https://znanium.ru/catalog/document?id=426496"

# page = requests.get(url)
# soup = BeautifulSoup(page.text, "html.parser")

# bibl_data = soup.find_all('pan', id="doc-biblio-card")

# print(bibl_data[0].text)

from app.books import BookParser, MDParser, YamlCreator, ParseShedule
from app.data_parser import *

url = "https://znanium.ru/catalog/document?id=426496"
# data = BookParser(url)

# data = MDParser(path_md='projects/databases.md')

# print(data.find_data())
# for item in data.find_data():
#     print(item.text)
# print(data.page)

# data = YamlCreator('projects/databases.yaml')
# print(data._data)
path = "C:/Users/Юрий Солдатов/YandexDisk/ИБИС/3-ИТ-09.03.02_24_00.xlsx"
shedule = ParseShedule(path, name='План')
shedule.search_code('Б1.О.10')
print(shedule.row_index)