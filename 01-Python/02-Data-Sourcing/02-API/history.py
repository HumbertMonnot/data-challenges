# pylint: disable=missing-docstring

import sys
import csv
import requests


from weather import search_city


def daily_forecast(woeid, year, month, day):
    """ return list of forecast for a specific day """
    url = f"https://www.metaweather.com/api/location/{woeid}/{year}/{month}/{day}"
    return requests.get(url).json()

def monthly_forecast(woeid, year, month):
    """ return a `list` of forecasts for the whole month """
    forecast_month = []
    for day in range(1,29):
        forecast_month += daily_forecast(woeid, year, month, day)
    if month == 2:
        return forecast_month
    for day in range(29,31):
        forecast_month += daily_forecast(woeid, year, month, day)
    if month in [4, 6, 9, 11]:
        return forecast_month
    forecast_month += daily_forecast(woeid, year, month, 31)
    return forecast_month


def write_csv(woeid, year, month, city, forecasts):
    """ dump all the forecasts to a CSV file in the `data` folder """
    name_file = f"data/{year}_{month:02}_{woeid}_{city}.csv"
    with open(name_file, 'w', encoding = 'utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=forecasts[0].keys())
        writer.writeheader()
        for forecast in forecasts:
            writer.writerow(forecast)

def main():
    if len(sys.argv) > 2:
        city = search_city(sys.argv[1])
        if city:
            woeid = city['woeid']
            year = int(sys.argv[2])
            month = int(sys.argv[3])
            if 1 <= month <= 12:
                forecasts = monthly_forecast(woeid, year, month)
                if not forecasts:
                    print("Sorry, could not fetch any forecast")
                else:
                    write_csv(woeid, year, month, city['title'], forecasts)
            else:
                print("MONTH must be a number between 1 (Jan) and 12 (Dec)")
                sys.exit(1)
    else:
        print("Usage: python history.py CITY YEAR MONTH")
        sys.exit(1)


if __name__ == '__main__':
    main()
