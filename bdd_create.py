#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import pymysql.cursors
import sys
import requests, json

#import personnal module
import classes as cl

FILE_CREATE = """DROP DATABASE IF EXISTS openfoodfacts;

CREATE DATABASE openfoodfacts CHARACTER SET 'utf8';

USE openfoodfacts;

CREATE TABLE IF NOT EXISTS Food(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(150) NOT NULL,
	categories_id VARCHAR(400) NOT NULL,
	nutri_score CHAR(1),
	url VARCHAR(150),
	stores VARCHAR(150),
	PRIMARY KEY(id)
	)ENGINE=InnoDB;
	
CREATE TABLE IF NOT EXISTS Categories(
	id VARCHAR(500) NOT NULL,
	name VARCHAR(100) NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Backup(
	id INT UNSIGNED AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	substitute_id INT UNSIGNED NOT NULL,
	PRIMARY KEY(id)
	)ENGINE=InnoDB;
	
"""

URL0 = "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux/1.json"
URL2 = "https://fr.openfoodfacts.org/categories.json"


#connection à la base de données
conn = pymysql.connect(host='localhost', user='root', passwd='', db='Openfoodfacts', charset='utf8')
cursor = conn.cursor()



def get_data_from_api(url):
    """Take an url and return data"""
    data = requests.get(url)
    data.encoding = "utf8"
    return data.json()


def fill_categories_table(url):
    """Fonction servant à remplir les tableaux de catégories, avec les données de catégories de OFF"""
    data_from_api = get_data_from_api(URL2)

    for data in data_from_api["tags"]:
        if data["products"] > 500 and "en:" in data["id"]: #Don't take the categories with to few products and
            try:
                category = cl.Categories(data)
                if "en:" in category.name or "fr:" in category.name:
                    pass
                else:
                    cursor.execute("INSERT INTO Categories (id, name)"\
                        "VALUES (%s, %s)", (category.id, category.name))
                    conn.commit()
                    print("Catégorie correctement insérée")
            #Don't take the non utf-8 data
            except conn.OperationalError:     
                pass

            

def insert_product(url):    
    data_from_api = get_data_from_api(URL0)
    
    for data in data_from_api["products"]:
        try:
            nutri_values = ["a", "b", "c", "d", "e"]
            nutri_score = []
            for nutri_values in data_from_api["nutrition_grade_fr"]:
                nutri_score.append(data.upper())
                return food.nutri_score          
        except KeyError:
            str_nutr_grade = "N/A"
            nutriscore = 0
        try:
            food = cl.Food(data)
            cursor.execute("INSERT INTO Food (name, categories_id, nutri_score, url, stores)"\
                           "VALUES (%s, %s, %s, %s, %s)",
                           (food.name, food.category, food.nutri_score, food.url, food.stores))
            conn.commit()
            print("Produit correctement insérée")            
        except conn.OperationalError: #Don't take the products with encoding error
            pass
        except KeyError: #Don't take lignes without 'product_name'
            pass
        except AttributeError: #Don't take products with 0 categories
            pass
        except conn.IntegrityError: #Don't take the products with an category unknow in the database
            pass
        except conn.DataError: #Pass when product name is too long
            pass
        
            


def main():
    """Main function, lauching the script"""
    #Call the sql script to create the database
    cursor.execute(FILE_CREATE)
    print("Base de données Openfoodfacts créé avec succès !")

    cursor.execute('use openfoodfacts;')
    fill_categories_table(URL2)
    for i in range(1, 1724): #1724 Nombre de page de la catégorie
        url_food = URL0+str(i)+'.json'
        insert_product(url_food)
    print("Base de données Openfoodfacts remplie avec succès !")


                
main()



