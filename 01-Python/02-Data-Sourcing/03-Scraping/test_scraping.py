#pylint: disable=missing-docstring,invalid-name
#pylint: disable=missing-docstring,line-too-long

from bs4 import BeautifulSoup

with open("pages/carrot.html", encoding="utf-8") as lien:
    soup = BeautifulSoup(lien, "html.parser")

for recipe in soup.find_all('p', class_= 'recipe-name'):
    print(recipe.text)
