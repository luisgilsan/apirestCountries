import requests


REGIONS_URL = 'https://restcountries-v1.p.rapidapi.com/all'
HEADERS = {
    'x-rapidapi-key': '21dd1342cemshbf299c12fd977dfp19f24ajsn98d0fe8cff3f',
    'x-rapidapi-host': 'restcountries-v1.p.rapidapi.com'
}
COUNTRIES_URL = 'https://restcountries.eu/rest/v2/region/'
         
def getRegions():
    r = requests.get(REGIONS_URL, headers=HEADERS)
    return r

def getCountries(region):
    url = COUNTRIES_URL + region.lower()
    r = requests.get(url)
    return r

