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
ALTER TABLE Backup ADD CONSTRAINT fk_produit_id FOREIGN KEY (produit_id) REFERENCES Food(id);
ALTER TABLE Backup ADD CONSTRAINT fk_substitut_id FOREIGN KEY (substitut_id) REFERENCES Food(id);

"""

CATEGORIES = ["https://fr.openfoodfacts.org/categorie/biscuits-aperitifs/", \
              "https://fr.openfoodfacts.org/categorie/Boeuf/", \
              "https://fr.openfoodfacts.org/categorie/Chips/", \
              "https://fr.openfoodfacts.org/categorie/Legumes-frais/", \
              "https://fr.openfoodfacts.org/categorie/Patisseries/"]

nouvelle_liste_url = []
url_format = []

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
    data_from_cat = {}
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


def remplir_table_categorie2():
    page_cat_data = recup_data_api()
    valeur = list(page_cat_data.values())

    # print("le nombre d'items est:")
    # print(len(valeur))
    # print("Le type de 'valeur' est:")
    # print(type(valeur))
    print(valeur[1])
    for i in CATEGORIES:
        liste_url = set(valeur[1]).intersection(CATEGORIES)  # comparer deux listes
        print(liste_url)

    # for value in page_cat_data:
    #     valeur = list(page_cat_data)
    # print("le nombre d'items est:")
    # print(len(valeur))
    #
    # print("Le type de 'valeur' est:")
    # print(type(valeur))
    #
    # print("valeur1: \n")
    # print(valeur[0])
    # print("valeur: \n")
    # print(valeur[1])

    # for key, value in valeur.iteritems():
    #     val = value
    #     cle = key
    #     data_cle.append(cle)
    #     data_value.append(val)
    # print(data_value)

    #
    # print("Le type de valeur est:")

    # for i in range(0,2):
    #     print("valeur: \n")
    #     print(valeur[i])
    # print(type(valeur))

    # print(valeur)

    # liste_url = set(liste_valeur).intersection(CATEGORIES) # comparer deux listes

    #     for url in valeur:
    #
    #         print(url)
    #
    #     for elt in range(len(CATEGORIES)):
    #         if str(valeur) in CATEGORIES[elt]:
    #             url_cle.append(str(valeur))
    #             print ("remplissage de la liste")
    #
    #     for i in CATEGORIES:
    #         for j in url_cle:
    #             liste_url.append(set(i).intersection(j))
    #             # if [j] in url_cle == [i] in CATEGORIES:
    #             #     liste_url.append(url_cle)
    #         else:
    #             pass
    #
    # print("Il y a:{} url en tout".format(len(url_cle)))
    # print("la liste:")
    # print(liste_url)
    # print("Il y a : {} url dans la liste".format(nombre_durl))

    # for i in page_cat_data["tags"][0]["url"]:
    #     return "url"

    # print (page_cat_data)
    # for i in CATEGORIES:
    #     for cle in page_cat_data:
    #         print(cle)
    #         if page_cat_data["tags"][0]["url"] == CATEGORIES[i]:
    #             liste_url().append(keys)
    #             print(liste_url)


def lister_url():
    data_from_list = {}
    for elt in CATEGORIES:  # pour chaque elt de ma liste
        # print(elt)
        for i in range(1, 3):  # generation d'un boucle avec i comme iterateur de 0 à 1133
            nouvelle_liste_url.append('{0}{1}.json'.format(elt, str(
                i)))  # formatage des url 1133 fois(nombre de pages max dans une catégories)\
            # + ajout à nouvelle liste
            # print(str(nouvelle_liste_url))
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
            if "en:" in ["categories"]:  # On ne prend pas celles en anglais
                pass
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
                category = food.category.split(",")

                cursor.execute("INSERT INTO Food (name, categories_id, nutri_score, url, stores)" \
                               "VALUES (%s, %s, %s, %s, %s)",
                               (food.name, category[0], food.nutri_score, food.url, food.stores))
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


if __name__ == "__main__":
    main()
