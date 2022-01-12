# pylint: disable=missing-docstring,line-too-long
import sys
from os import path
import csv
from bs4 import BeautifulSoup
import requests

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html, "html.parser")
    recipes = soup.find_all("div", class_="p-2 recipe-details")
    list_recipes =[]
    for recipe in recipes :
        name = recipe.find("p").string
        elements = recipe.find("div").find_all("small")
        prep_time = elements[0].find("span").string
        difficulty = elements[1].find("span").string
        list_recipes.append({"name":name,"difficulty":difficulty,"prep_time":prep_time})
    return list_recipes

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    name_csv = f"recipes/{ingredient}.csv"
    with open(name_csv, 'a', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        writer.writeheader()
        for recipe in recipes:
            writer.writerow(recipe)

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    url = f"https://recipes.lewagon.com/?search[query]={ingredient}&button=&page={start}"
    return requests.get(url, allow_redirects=False).content

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file, encoding="utf-8")
    print(f'curl "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        for k in range(1,6):
            recipes = parse(scrape_from_internet(ingredient,k))
            write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
