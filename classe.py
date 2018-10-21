#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""This file contains the classes of this program"""


class Categories():
    """Class representing the 'Categories' table of the database"""

    def __init__(self, data_from_off, index=None):
        """Initiate a dictionary for argument"""
        # Use the key when creating the database from the OFF API
        try:
            self.id = data_from_off["id"]
            self.name = data_from_off["name"]
            # Use the index when calling the class from the program
        except TypeError:
            self.id = data_from_off
            self.name = data_from_off[0]
            self.index = index


class Food():
    """Class representing the 'Food' table of the database"""

    def __init__(self, data_from_off, index=None):
        """Initiate a dictionary for argument"""

        # Use the key when creating the database from the OFF API
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

