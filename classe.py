#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Ce fichier contient des classes représentant la base de données de ce programme"""


class Categories():
    """Classe représentant la table 'Categories' de la base de données"""

    def __init__(self, data_from_off, index=None):
        """Initier un dictionnaire pour argument"""
        # Utiliser la clé lors de la création de la base de données à partir de l'API OFF
        try:
            self.id = data_from_off["id"]
            self.name = data_from_off["name"]
        # Utilisez l'index lorsque l'on appel la classe depuis le programme
        except TypeError:
            self.id = data_from_off
            self.name = data_from_off[0]
            self.index = index


class Food():
    """Classe représentant la table 'Food' de la base de données"""

    def __init__(self, data_from_off, index=None):
        """Initier un dictionnaire pour argument"""

        # Utiliser la clé lors de la création de la base de données à partir de l'API OFF
        try:
            self.name = data_from_off["product_name"]
            try:
                self.category = data_from_off["categories"]

            except IndexError:
                pass
            try:
                self.nutri_score = data_from_off["nutrition_grade_fr"]
            except KeyError:
                self.nutri_score = "None"
            try:
                self.stores = data_from_off["stores"]
            except KeyError:
                self.stores = " "
            try:
                self.url = data_from_off["url"]
            except KeyError:
                self.url = "Url not available"
        except IndexError:
            pass
        except TypeError:
            self.id = data_from_off
            self.name = data_from_off[1]
            self.category = data_from_off[2]
            self.nutri_score = data_from_off[3]
            self.stores = ""
            try:
                self.stores = data_from_off[5]
            except IndexError:
                pass
            try:
                self.url = data_from_off[4]
            except IndexError:
                self.url = data_from_off
            self.index = index

