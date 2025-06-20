from bs4 import BeautifulSoup
import requests

url = "https://znanium.ru/catalog/document?id=426496"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

bibl_data = soup.find_all('pan', id="doc-biblio-card")

print(bibl_data[0].text)