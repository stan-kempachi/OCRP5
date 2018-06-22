#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""project script 5"""

# import modules
import json
import requests
import pymysql.cursors

#Constant of this script
CATEGORIES_URL = 'https://fr.openfoodfacts.org/categories.json'
FOOD_URL = 'https://world.openfoodfacts.org/country/france/'

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='openfoodfacts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def get_data_from_api(url):
    """Take an url and return data"""
    data = requests.get('https://fr.openfoodfacts.org/categories.json')
    return data.json()
    data2 = requests.get('https://world.openfoodfacts.org/country/france/')
    return data.json()


