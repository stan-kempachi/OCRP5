#!/usr/bin/env python
# -*- coding: utf-8 -*-


# import pip module
import pymysql.cursors
import requests, json

# import personnal module
import Classe as cl

FILE_CREATE = """DROP DATABASE IF EXISTS openfoodfacts;
CREATE DATABASE openfoodfacts CHARACTER SET 'utf8';
USE openfoodfacts;
CREATE TABLE Food(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    categories_id VARCHAR(500) NOT NULL,
    nutri_score CHAR(1),
    url VARCHAR(150),
    stores VARCHAR(150),
    PRIMARY KEY(id)
    )ENGINE=InnoDB;

CREATE TABLE Categories(
    id VARCHAR(500) NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id)
    )ENGINE=InnoDB;
CREATE TABLE Backup(
    id INT UNSIGNED AUTO_INCREMENT,
    produit_id INT UNSIGNED NOT NULL,
    substitut_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(id)
    )ENGINE=InnoDB;

ALTER TABLE Categories ADD UNIQUE INDEX(name);
ALTER TABLE Food ADD UNIQUE INDEX(name);
ALTER TABLE Backup ADD CONSTRAINT fk_produit_id FOREIGN KEY (produit_id) REFERENCES Food(id);
ALTER TABLE Backup ADD CONSTRAINT fk_substitut_id FOREIGN KEY (substitut_id) REFERENCES Food(id);

"""

CATEGORIES = ["https://fr.openfoodfacts.org/categorie/veloutes/", \
              "https://fr.openfoodfacts.org/categorie/sandwichs-garnis-de-charcuteries/", \
              "https://fr.openfoodfacts.org/categorie/gratins/", \
              "https://fr.openfoodfacts.org/categorie/nouilles-instantanees/", \
              "https://fr.openfoodfacts.org/categorie/batonnets-glaces/"]

nouvelle_liste_url = []

# connection à la base de données
conn = pymysql.connect(host='localhost', user='root', passwd='', db='Openfoodfacts', charset='utf8')
cursor = conn.cursor()


def recup_data_api(url):
    """Take an url and return data"""
    data = requests.get(url)
    data.encoding = "utf8"
    return data.json()
    print(data)


def remplir_table_categorie():
    url_format = []
    for elt in CATEGORIES:  # pour chaque elt de ma liste
        url_format.append(elt + (str(".json")))
    print(url_format)
    for elt in url_format:
        data_from_cat = recup_data_api(elt)
        for data in data_from_cat["products"]:
            if "categories" in data and "en:" in "categories":  # On ne prend pas celles en anglais
                pass
            else:
                try:
                    category = cl.Categories(data)

                    name = category.name.split(",")

                    if "en:" in category.name or "fr:" in category.name or "de:" in category.name:
                        pass

                    else:
                        cursor.execute("INSERT INTO Categories (id, name)" \
                                       "VALUES (%s, %s)", (category.id, name[0]))

                        conn.commit()
                        print("Catégorie correctement insérée")
                # Don't take the non utf-8 data
                except (conn.OperationalError, conn.DataError, conn.IntegrityError, KeyError):
                    pass


def lister_url():
    data_from_list = []
    for elt in CATEGORIES:  # pour chaque elt de ma liste
        for i in range(1, 16):  # generation d'un boucle avec i comme iterateur de 0 à 15 (311 produits max)
            nouvelle_liste_url.append('{0}{1}.json'.format(elt, str(
                i)))  # ajout à nouvelle liste



def insert_product():
    for elt in nouvelle_liste_url:
        print(elt)
        data_from_list = recup_data_api(elt)

        for data in data_from_list["products"]:
            if "en:" in ["categories"]:  # On ne prend pas celles en anglais
                pass
        for data in data_from_list["products"]:
            for rows in ['categories_tags']:
                    if 'fr:' in rows:
                        rows.replace("-"," ")
                        return food.category
            try:
                nutri_values = ["a", "b", "c", "d", "e"]
                nutri_score = []
                for nutri_values in data_from_list["nutrition_grade_fr"]:
                    nutri_score.append(nutri_values)
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
            except (conn.OperationalError, conn.DataError, conn.IntegrityError, KeyError, AttributeError):
                pass


def main():
    """Main function, lauching the script"""
    # Call the sql script to create the database
    cursor.execute(FILE_CREATE)
    print("Base de données Openfoodfacts créé avec succès !")

    cursor.execute('use openfoodfacts;')
    lister_url()
    remplir_table_categorie()
    insert_product()
    print("Base de données Openfoodfacts remplie avec succès !")


if __name__ == "__main__":
    main()


