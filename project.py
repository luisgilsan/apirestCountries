from api import getRegions, getCountries
from datetime import datetime
import hashlib
import json
import pandas as pd
import sqlite3
import os
import pathlib

COLUMNS = ['Region','CityName','Languaje','Time']

def createDatabase(df):
    con = sqlite3.connect("db.sqlite3")
    try:
        cursor = con.cursor()
        cursor.execute("DROP TABLE countries")
    except:
        pass
    df.to_sql(name='countries', con=con)

def getListCountries(response):
    response = getRegions()
    json_data = json.loads(response.text)
    regions = []
    for value in json_data:
        region = value.get('region','')
        if region not in regions and region != '':
            regions.append(region)
    return regions

def getCountriebyRegion(region_list):
    countries = []
    for region in region_list:
        start_time = datetime.now()
        response = getCountries(region)
        if response.status_code == 200:
            countrie = json.loads(response.text)[0]
            countrie_name = countrie.get('name','')
            countrie_lang = countrie['languages'][0].get('iso639_1','')
            hash_object = hashlib.sha1(bytes(countrie_lang, 'utf-8'))
            lang_sha1 = hash_object.hexdigest()
            end_time = datetime.now()
            diff = end_time - start_time
            countries.append([region,countrie_name, lang_sha1, round(diff.microseconds/1000,0)])
    return countries

def countriesToDataframe(values):
    df = pd.DataFrame(values, columns=COLUMNS)
    return df

def printDataframeTimes(df):
    print('Tiempo total: ' + str(df["Time"].sum()))
    print('Tiempo promedio: ' +str( round(df["Time"].mean(),0)) )
    print('Tiempo mínimo: ' +str( round(df["Time"].min(),0)) )
    print('Tiempo máximo: ' +str( round(df["Time"].max(),0)) )

def createJsonFile(df):
    # directory_path = os.path.abspath(os.getcwd())
    directory_path = pathlib.Path().resolve()
    print(directory_path)
    jsondata = df.to_json('data.json')

def dataProcess():
    response = getRegions()
    region_list = getListCountries(response)
    countries = getCountriebyRegion(region_list)
    df = countriesToDataframe(countries)
    createDatabase(df)
    createJsonFile(df)

dataProcess()