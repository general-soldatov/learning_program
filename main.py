from bs4 import BeautifulSoup
import requests

# url = "https://znanium.ru/catalog/document?id=426496"

# page = requests.get(url)
# soup = BeautifulSoup(page.text, "html.parser")

# bibl_data = soup.find_all('pan', id="doc-biblio-card")

# print(bibl_data[0].text)

from app.books import BookParser, MDParser

# url = "https://znanium.ru/catalog/document?id=426496"
# data = BookParser(url)

data = MDParser(path_md='projects/databases.md')
print(data.find_data)

print(data.find_data())