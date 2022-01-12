# pylint: disable=missing-module-docstring

import sys
import requests

BASE_URI = "https://www.metaweather.com"


def search_city(query):
    '''Look for a given city and disambiguate between several candidates.Return a city (or None)'''
    url = f"https://www.metaweather.com/api/location/search/?query={query}"
    response = requests.get(url).json()
    if response == []:
        return None
    if len(response)==1:
        return response[0]
    for k, city in enumerate(response,start = 1) :
        print(f"{k} : {city['title']}")
    index = int(input("Numéro de la ville : "))-1
    return response[index]

def weather_forecast(woeid):
    '''Return a 5-element list of weather forecast for a given woeid'''
    url = f"https://www.metaweather.com/api/location/{woeid}"
    response = requests.get(url).json()
    days = response['consolidated_weather']
    weather_5 = []
    for k in range(5):
        dico = {'applicable_date' : days[k]['applicable_date'],
             'weather_state_name' : days[k]['weather_state_name'],
            'max_temp' : days[k]['max_temp']}
        weather_5.append(dico)
    return weather_5

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    woeid = city['woeid']
    weather = weather_forecast(woeid)
    for day in weather:
        print(f"{day['applicable_date']}: {day['weather_state_name']} {day['max_temp']:.1f}°C")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
