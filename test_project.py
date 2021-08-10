from api import getRegions, getCountries
from project import getListCountries
import pytest

def testsRegionsApi():
    response = getRegions()
    assert response.status_code == 200

def testsCountriesApi():
    response = getCountries('africa')
    assert response.status_code == 200

def testRegionsList():
    response = getRegions()
    countries_list = getListCountries(response)
    assert len(countries_list) > 0 