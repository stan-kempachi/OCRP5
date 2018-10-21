#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors
import classe as cl


# connection to the database
conn = pymysql.connect(host='localhost', user='root', passwd='', db='Openfoodfacts', charset='utf8')
cursor = conn.cursor()


def select_categories(dict_categories):
    category0 = ("veloutes")
    category1 = ("sandwichs garnis de charcuteries")
    category2 = ("gratins")
    category3 = ("yaourts a boire")
    category4 = ("batonnets glaces")
    cursor.execute("""USE Openfoodfacts""")
    cursor.execute("""SELECT name FROM Categories\
    WHERE name LIKE %s OR name LIKE %s OR name LIKE %s OR name LIKE %s OR name LIKE %s""", \
                   (category0, category1, category2, category3, category4))
    categories = cursor.fetchall()

    # fill in the dict_categories with the five categories
    print("Voici les 5 catégories permettant une recherche:")
    index = 1
    for i in categories:
        categories_affich = cl.Categories(i, index)
        dict_categories[categories_affich.index] = (categories_affich.name, categories_affich.id)
        print(index, " : ", categories_affich.name)
        index += 1
    return dict_categories


def find_a_susbstitut():
    "" "The user can choose a product from a list and our application will return a substitute" ""
    dict_categories = {}
    dict_product = {}
    # Search for a product until it matches the chosen category
    while len(dict_product) == 0:
        while dict_categories == {}:
            select_categories(dict_categories)
        choice = user_choix_input(len(dict_categories))

        # Display a list of products in the chosen category
        # The user must choose a product

        print(" Vous avez choisi la categorie: {}".format(dict_categories[choice][0]))

        dict_product = poster_list_products(select_products(dict_categories[choice][0]))

        if len(dict_product) == 0:
            print("\n Il n'y a pas de produits pour cette catégorie... \n")
            dict_categories = {}

    choice = user_choix_input(len(dict_product))

    chosen_product = extract_product(dict_product[choice])

    # Display the description of the chosen product
    print('\n Vous avez choisi ce produit : \n')
    print_product(chosen_product)

    # Find a substitute and display it
    try:
        substitute = search_substitute(chosen_product)
        print('\n Vous pouvez remplacer ce produit par : \n')
        print_product(substitute)
        ajout_backup(chosen_product, substitute)
    except (AttributeError, TypeError):
        pass


def select_products(category):
    "" "Selects the BDD products contained in the user's chosen category" ""
    category = "%" + category + "%"
    cursor.execute('USE openfoodfacts;')
    cursor.execute(
        """SELECT DISTINCT id, name, categories_id, nutri_score, stores, url  FROM Food WHERE name LIKE %s or categories_id LIKE %s """,
        (category, category))
    products = cursor.fetchall()
    return products


def poster_list_products(products):
    """Use the result of the product selection function and display it """
    print('\n Choisir un produit : ')
    dict_product = {}
    index = 1

    for i in products:
        poster_products = cl.Food(i, index)
        dict_product[poster_products.index] = poster_products.name
        print(index, " : ", poster_products.name)
        index += 1
    return dict_product


def user_choix_input(number_of_choice):
    running = True
    while running is True:
        user_choice = input("Entrez le chiffre de votre choix ici: \n")
        try:
            int(user_choice)
            if int(user_choice) < 0 or int(user_choice) > number_of_choice:
                print("Vous devez entrer un chiffre dans la selection")
            else:
                running = False
                return int(user_choice)
        except ValueError:
            print("Ceci n'est pas un chiffre, vous devez entrer un chiffre")


def print_product(product):
    """Takes a product and displays its characteristics"""
    try:
        print("\n \
        Name : {} \n \
        Categories : {} \n \
        Nutri-score : {} \n \
        Store : {} \n \
        URL : {}".format(product.name, product.category, product.nutri_score, product.stores, product.url))
    except TypeError:
        print("Désolé, il n'y a pas de substitut pour ce product...")


def ajout_backup(product, substitute):
    """Add the chosen product and its substitute to the TABLE Backup in the database"""

    print('\n Voulez-vous enregistrer cette comparaison comme favori ?')
    print('1. Oui')
    print('2. Non')
    choix = user_choix_input(2)
    if choix == 1:
        cursor.execute('USE openfoodfacts;')
        cursor.execute("""INSERT INTO Backup (produit_id, substitut_id) \
            VALUES (%s,%s)""", (product.id[0], substitute.id[0]))
        conn.commit()
        print('Sauvergarde effectuée')
    elif choix == 2:
        print('Non sauvegardé')


def poster_product_list(product):
    """Use the result of the product selection function and display it"""
    print('\n Séléctionner un product : ')
    dict_produit = {}
    index = 1
    for i in product:
        poster_product = cl.Food(i, index)
        dict_produit[poster_product.index] = poster_product.name
        print(index, " : ", poster_product.name)
        index += 1
    return dict_produit


def search_substitute(product):
    """Find a product substitute in the database"""
    cursor.execute('USE openfoodfacts;')
    # Make a string with the categories used in the query
    search = product.category
    # Other variable
    product_name = product.name
    product_score = product.nutri_score

    cursor.execute("""SELECT Food.id, Food.name, categories_id, nutri_score, url, stores \
     FROM Food \
     INNER JOIN Categories ON Food.categories_id = Categories.name\
     WHERE categories_id LIKE %s AND Food.name NOT LIKE %s \
     AND Food.nutri_score <= %s """, (search, product_name, product_score))
    substitute = cursor.fetchone()
    try:
        return cl.Food(substitute)
    except TypeError:
        print("Désolé, il n'y a pas de substitut pour ce product...")


def extract_product(product):
    """Take the name of a product and return an object containing the specifications of this product"""
    product = "%" + product + "%"
    cursor.execute("USE openfoodfacts;")
    cursor.execute("""SELECT Food.id, Food.name, categories_id, nutri_score, url, stores \
     FROM Food \
     INNER JOIN Categories ON Food.categories_id LIKE Categories.name\
     WHERE Food.name LIKE %s;""", (product))
    product = cursor.fetchone()
    product_class = cl.Food(product)
    return product_class


def affiche_favoris():
    """Afficher tous les favoris de l'utilisateur"""
    # Liste des favoris utilisés pour la fonction "select_favorite"
    favorite_dict = {}
    # pour les produits dans Count
    cursor.execute('USE openfoodfacts;')
    cursor.execute("""SELECT F1.name as Product, F2.name as Substitute \
        FROM Backup \
        INNER JOIN Food F1 ON Backup.produit_id = F1.id     
        INNER JOIN Food F2 ON Backup.substitut_id = F2.id""")
    favorite = cursor.fetchall()
    index = 1
    for i in favorite:
        favorite_tuple = (i[0], i[1])
        print("\n {}. {}, Peut être remplacé par {}.".format(index, \
                                                             favorite_tuple[0], favorite_tuple[1]))
        favorite_dict[index] = favorite_tuple
        index += 1

    if not favorite_dict:
        print ("La liste des favoris est vide.")
    else:
        print('Choisissez un chiffre pour plus de détail.')
        select_favorite(favorite_dict)


def select_favorite(favoris_dict):
    """Display the information of the product and the substitute"""
    choice = user_choix_input(len(favoris_dict))
    # Extract the specifitions of the product to display it
    product = extract_product(favoris_dict[choice][0])
    # Extract the specifitions of the substitute to display it
    substitute = extract_product(favoris_dict[choice][1])
    print_product(product)
    print('\n Vous pouvez remplacer ceci par: \n')
    print_product(substitute)


def main():
    """Fonction main du programme"""
    print('Bienvenu sur notre application !')
    running = True
    while running is True:
        print(" _________________________________________ ")
        print('|_____________MENU PRINCIPAL_____________|\n')
        print('1. Choisir des aliments et les remplacer ?')
        print('2. Retrouver mes aliments substitués.')
        print('3. Exit.')
        choix = user_choix_input(3)
        if choix == 1:
            find_a_susbstitut()
        elif choix == 2:
            affiche_favoris()
        elif choix == 3:
            running = False


if __name__ == "__main__":
    main()
