# pylint: disable=missing-docstring

import csv

COUNTRIES_FILEPATH = "data/dictionary.csv"
MEDALS_FILEPATH = "data/winter.csv"


def most_decorated_athlete_ever():
    """Returns who won the most winter olympic games medals (gold/silver/bronze) ever"""
    with open('data/winter.csv', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        winner_medal = {}
        for row in reader:
            if winner_medal.get(row['Athlete'],0) == 0:
                winner_medal[row['Athlete']] =1
            else :
                winner_medal[row['Athlete']] += 1
        best_athletes = max(winner_medal, key=lambda key: winner_medal[key])
        return best_athletes

def country_with_most_gold_medals(min_year, max_year):
    """Returns which country won the most gold medals between `min_year` and `max_year`"""
    with open('data/winter.csv', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        best_country = {}
        for row in reader:
            if int(row['Year']) >= min_year and int(row['Year']) <= max_year \
            and row['Medal']=='Gold':
                if best_country.get(row['Country'],0) == 0:
                    best_country[row['Country']] =1
                else :
                    best_country[row['Country']] += 1
        the_best_country =  max(best_country, key=lambda key: best_country[key])
    with open('data/dictionary.csv', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader :
            if row["Code"]==the_best_country:
                long_best_country = row["Country"]
    return long_best_country

def top_three_women_in_five_thousand_meters():
    """Returns the three women with the most 5000 meters medals(gold/silver/bronze)"""
    with open('data/winter.csv', encoding = 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        women_5000 = {}
        for row in reader:
            if row['Gender'] == 'Women' and row['Event'] == '5000M':
                if women_5000.get(row['Athlete'],0) == 0:
                    women_5000[row['Athlete']] =1
                else :
                    women_5000[row['Athlete']] += 1
    list_athletes = []
    for _ in range(3):
        list_athletes.append(max(women_5000, key=lambda key: women_5000[key]))
        del women_5000[max(women_5000, key=lambda key: women_5000[key])]
    return list_athletes
