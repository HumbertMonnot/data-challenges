# pylint: disable=no-value-for-parameter
"""
Client of the Wagon OpenGraph API
"""

import requests

def fetch_metadata(url):
    """
    Return a dictionary of OpenGraph metadata found in HTML of given url
    """
    url2 = f"""https://opengraph.lewagon.com/?url={url}"""
    response = requests.get(url2)
    if response.status_code != 200:
        return ""
    return response.json()['data']

#To manually test, please uncomment the following lines and run `python opengraph.py`:
#import pprint
#pp = pprint.PrettyPrinter(indent=4)
#print(fetch_metadata("https://www.lewagon.com"))
