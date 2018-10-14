#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors
import re
import Classe as cl

# connection à la base de données
conn = pymysql.connect(host='localhost', user='root', passwd='', db='Openfoodfacts', charset='utf8')
cursor = conn.cursor()


def select_categories(dict_categories):
    recherche_utilisateur = ""

    category0 = ("veloutes")
    category1 = ("sandwichs")
    category2 = ("gratins")
    category3 = ("nouilles instantanees")
    category4 = ("batonnets glaces")
    cursor.execute("""USE Openfoodfacts""")
    cursor.execute("""SELECT name FROM Categories\
    WHERE name LIKE %s OR name LIKE %s OR name LIKE %s OR name LIKE %s OR name LIKE %s""", \
                   (category0, category1, category2, category3, category4))
    categories = cursor.fetchall()

    # remplir le dict_categories avec le resultat de la recherche
    print("Voici les 5 catégories permettant une recherche:")
    index = 1
    for i in categories:
        categories_affich = cl.Categories(i, index)
        dict_categories[categories_affich.index] = (categories_affich.name, categories_affich.id)
        print(index, " : ", categories_affich.name)
        index += 1
    return dict_categories


def trouver_un_susbstitut():
    """L'utilisateur peut choisir un produit dans une liste et notre application retournera un substitut"""
    dict_categories = {}
    dict_produit = {}
    # Recherche d'un produit jusqu'à ce qu'il corresponde à la catégorie choisie
    while len(dict_produit) == 0:
        while dict_categories == {}:
            select_categories(dict_categories)
        choix = user_choix_input(len(dict_categories))

        # Affiche une liste de produits contenus dans la catégorie choisie
        # L'utilisateur doit choisir un produit

        print(" Vous avez choisi la categorie: {}".format(dict_categories[choix][0]))

        dict_produit = affiche_liste_produits(select_produits(dict_categories[choix][0]))

        if len(dict_produit) == 0:
            print("\n Il n'y a pas de produits pour cette catégorie... \n")
            dict_categories = {}

    choix = user_choix_input(len(dict_produit))

    produit_choisi = extraire_produit(dict_produit[choix][1])

    # Afficher la description du produit choisi
    print('\n Vous avez choisi ce produit : \n')
    print_produit(produit_choisi)

    # Rechercher un substitut et l'afficher
    print('\n Vous pouvez remplacer ce produit par : \n')
    substitut = recherche_substitut(produit_choisi)
    try:
        print_produit(substitut)
        ajout_backup(produit_choisi, substitut)
    except AttributeError:
        pass


def select_produits(category):
    """Selectionne les produits de la BDD contenus dans la catégories choisie par l'utilisateur"""
    category = "%" + category + "%"
    cursor.execute('USE openfoodfacts;')
    cursor.execute(
        """SELECT DISTINCT id, name, categories_id, nutri_score, stores, url  FROM Food WHERE name LIKE %s or categories_id LIKE %s """,
        (category, category))
    produits = cursor.fetchall()
    return produits


def affiche_liste_produits(produits):
    """
Utiliser le résultat de la fonction de sélection des produits et l'afficher"""
    print('\n Choisir un produit : ')
    dict_produit = {}
    index = 1

    for i in produits:
        affiche_produits = cl.Food(i, index)
        dict_produit[affiche_produits.index] = affiche_produits.name
        print(index, " : ", affiche_produits.name[1])
        index += 1
    return dict_produit


def user_choix_input(nombre_de_choix):
    marche = True
    while marche is True:
        user_choix = input("Entrez le chiffre de votre choix ici: \n")
        try:
            int(user_choix)
            if int(user_choix) < 0 or int(user_choix) > nombre_de_choix:
                print("Vous devez entrer un chiffre dans la selection")
            else:
                marche = False
                return int(user_choix)
        except ValueError:
            print("Ceci n'est pas un chiffre, vous devez entrer un chiffre")


def print_produit(produit):

    """Prend un produit et affiche ses caractéristiques"""
    print("\n \
    Name : {} \n \
    Categories : {} \n \
    Nutri-score : {} \n \
    Store : {} \n \
    URL : {}".format(produit.name[1], produit.category[2], produit.nutri_score[3], produit.stores[5], produit.url[4]))


def ajout_backup(produit, substitut):
    """Ajouter le produit choisi et son substitut à la TABLE Backup dans la base de données"""

    print('\n Voulez-vous enregistrer cette comparaison comme favori ?')
    print('1. Oui')
    print('2. Non')
    choix = user_choix_input(2)
    if choix == 1:
        cursor.execute('USE openfoodfacts;')
        cursor.execute("""INSERT INTO Backup (produit_id, substitut_id) \
            VALUES (%s,%s)""", (produit.id[0], substitut.id[0]))
        conn.commit()
        print('Sauvergarde effectuée')
    elif choix == 2:
        print('Non sauvegardé')


def affiche_liste_produit(produit):
    """Utiliser le résultat de la fonction de sélection de produit et l'afficher"""
    print('\n Séléctionner un produit : ')
    dict_produit = {}
    index = 1
    for i in produit:
        produits_affich = cl.Food(i, index)
        dict_produit[produits_affich.index] = produits_affich.name
        print(index, " : ", produits_affich.name)
        index += 1
    return dict_produit


def recherche_substitut(produit):

    """Rechercher un substitut du produit dans la base de données"""
    cursor.execute('USE openfoodfacts;')
    # Faire une chaîne avec la catégories, utilisées dans la requête
    recherche = produit.category[2]
    # Autre variable
    produit_name = produit.name[1]
    produit_score = produit.nutri_score[3]

    cursor.execute("""SELECT Food.id, Food.name, categories_id, nutri_score, stores, url \
     FROM Food \
     INNER JOIN Categories ON Food.categories_id = Categories.name\
     WHERE categories_id LIKE %s AND Food.name NOT LIKE %s \
     AND Food.nutri_score <= %s """, (recherche, produit_name, produit_score))
    substitut = cursor.fetchone()
    try:
        return cl.Food(substitut)
    except TypeError:
        print("Désolé, il n'y a pas de substitut pour ce produit...")

def extraire_produit(produit):
    """Prendre le nom d'un produit et renvoyer un objet
    contenant les spécifications de ce produit"""
    produit = "%" + produit + "%"
    cursor.execute("USE openfoodfacts;")
    cursor.execute("""SELECT Food.id, Food.name, categories_id, nutri_score, url, stores \
     FROM Food \
     INNER JOIN Categories ON Food.categories_id LIKE Categories.name\
     WHERE Food.name LIKE %s;""", (produit,))

    produit = cursor.fetchone()
    produit_class = cl.Food(produit)
    return produit_class


def affiche_favoris():
    """Afficher tous les favoris de l'utilisateur"""
    # Liste des favoris utilisés pour la fonction "select_favoris"
    favoris_dict = {}
    # pour les produits dans Count
    cursor.execute('USE openfoodfacts;')
    # cursor.execute('SELECT COUNT(*) FROM Backup;')
    # nb_favoris = cursor.fetchone()
    cursor.execute("""SELECT F1.name as Product, F2.name as Substitute \
        FROM Backup \
        INNER JOIN Food F1 ON Backup.produit_id = F1.id     
        INNER JOIN Food F2 ON Backup.substitut_id = F2.id""")
    favoris = cursor.fetchall()
    index = 1
    for i in favoris:
        favoris_tuple = (i[0], i[1])
        print("\n {}. {}, Peut être remplacé par {}.".format(index, \
                                                             favoris_tuple[0], favoris_tuple[1]))
        favoris_dict[index] = favoris_tuple
        index += 1
    print('Choisissez un chiffre pour plus de détail.')
    select_favoris(favoris_dict)


def select_favoris(favoris_dict):
    """Display the information of the product and the substitute"""
    choix = user_choix_input(len(favoris_dict))
    # Extract the specifitions of the product to display it
    produit = extraire_produit(favoris_dict[choix][0])
    # Extract the specifitions of the substitute to display it
    substitut = extraire_produit(favoris_dict[choix][1])
    print_produit(produit)
    print('\n Vous pouvez remplacer ceci par: \n')
    print_produit(substitut)


def main():
    """Fonction main du programme"""
    print('Bienvenu sur notre application!')
    marche = True
    while marche is True:
        print(" _________________________________________ ")
        print('|_____________MENU PRINCIPALE_____________|\n')
        print('1. Choisir des aliments et les remplacer?')
        print('2. Retrouver mes aliments substitués.')
        print('3. Exit.')
        choix = user_choix_input(3)
        if choix == 1:
            trouver_un_susbstitut()
        elif choix == 2:
            affiche_favoris()
        elif choix == 3:
            marche = False


if __name__ == "__main__":
    main()
