#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""project 5 script """

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

def get_category_api(self):
    """Take an url and return data"""
    r_data = requests.get('https://fr.openfoodfacts.org/categories.json')
    categ_json = r_data.json()
    add_category = ("INSERT INTO Category" "category" "VALUES (%s)")
    self.cursor.execute(add_category, categ_json)
    db.commit()
	

def get_food_api(self):
    r_data2 = requests.get('https://world.openfoodfacts.org/country/france/')
    food_json = r_data2.json()
	npProducts = r_data.count // 445
	nbPages = in(npProducts/20) + 1
    add_food = ("INSERT INTO Food " "")
    self.cursor.execute(add_food, food_json)
    db.commit()

