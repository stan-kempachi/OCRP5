#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

import pymysql.cursors
import sys
import requests, json

# import personnal module
from requests import Response

import Classe as cl

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
CATEGORIES = ["https://fr.openfoodfacts.org/categorie/aliments-a-base-de-fruits-et-de-legumes/", \
              "https://fr.openfoodfacts.org/categorie/biscuits-aperitifs/", \
              "https://fr.openfoodfacts.org/categorie/boissons/", \
              "https://fr.openfoodfacts.org/categorie/Boeuf/", \
              "https://fr.openfoodfacts.org/categorie/Chips/", \
              "https://fr.openfoodfacts.org/categorie/Desserts/", \
              "https://fr.openfoodfacts.org/categorie/Fromages/", \
              "https://fr.openfoodfacts.org/categorie/Legumes-frais/", \
              "https://fr.openfoodfacts.org/categorie/Patisseries/", \
              "https://fr.openfoodfacts.org/categorie/Surgeles/"]


nouvelle_liste_url = []  
url_format = []



# connection à la base de données
conn = pymysql.connect(host='localhost', user='root', passwd='', db='Openfoodfacts', charset='utf8')
cursor = conn.cursor()


def recup_data_api(url):
    """Take an url and return data"""
    data: Response = requests.get(url)
    data.encoding = "utf8"
    return data.json()
    print(data)



    

def remplir_table_categorie():
    data_from_cat = {}
    for elt in CATEGORIES:  # pour chaque elt de ma liste
        url_format.append(elt + (str(".json")))
    print(url_format)
    for elt in url_format:
        data_from_cat = recup_data_api(elt)
        #print (str(data_from_cat))
        for data in data_from_cat["products"]:
            if "categories" in data and "en:" in "categories":
                pass
            else:
                try:
                    category = cl.Categories(data)
                    if "en:" in category.name or "fr:" in category.name:
                        pass
                    else:
                        cursor.execute("INSERT INTO Categories (id, name)" \
                                       "VALUES (%s, %s)", (category.id, category.name))
                        conn.commit()
                        print("Catégorie correctement insérée")
                # Don't take the non utf-8 data
                except (conn.OperationalError, conn.DataError, conn.IntegrityError, KeyError):
                    pass


        


def lister_url():
    data_from_list = {}
    for elt in CATEGORIES:  # pour chaque elt de ma liste
        # print(elt)
        for i in range(1, 10):  # generation d'un boucle avec i comme iterateur de 0 à 1133
            nouvelle_liste_url.append('{0}{1}.json'.format(elt, str(i)))  # formatage des url 1133 fois(nombre de pages max dans une catégories)\
            # + ajout à nouvelle liste
            #print(str(nouvelle_liste_url))
    for elt in nouvelle_liste_url:  # pour chaque elt de
        print("récupération des produits en cours")
        recup_data_api(elt)
        return data_from_list
    print("Récupération terminée")


def insert_product():
    lister_url()
    for elt in nouvelle_liste_url:
        print(elt)
        data_from_list = recup_data_api(elt)        
        
        for data in data_from_list["products"]:
            try:
                nutri_values = ["a", "b", "c", "d", "e"]
                nutri_score = []
                for nutri_values in data_from_list["nutrition_grade_fr"]:
                    nutri_score.append(nutri_values.upper())
                return food.nutri_score
            except KeyError:
                str_nutr_grade = "N/A"
                nutriscore = 0
                pass
            try:
                food = cl.Food(data)
                cursor.execute("INSERT INTO Food (name, categories_id, nutri_score, url, stores)" \
                               "VALUES (%s, %s, %s, %s, %s)",
                               (food.name, food.category, food.nutri_score, food.url, food.stores))
                conn.commit()
                print("Produit correctement insérée")
            except conn.OperationalError:  # Don't take the products with encoding error
                pass
            except KeyError:  # Don't take lignes without 'product_name'
                pass
            except AttributeError:  # Don't take products with 0 categories
                pass
            except conn.IntegrityError:  # Don't take the products with an category unknow in the database
                pass
            except conn.DataError:  # Pass when product name is too long
                pass


def main():
    """Main function, lauching the script"""
    # Call the sql script to create the database
    cursor.execute(FILE_CREATE)
    print("Base de données Openfoodfacts créé avec succès !")

    cursor.execute('use openfoodfacts;')
    remplir_table_categorie()
    insert_product()
    print("Base de données Openfoodfacts remplie avec succès !")



main()
