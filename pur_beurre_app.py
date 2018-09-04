#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import personnal module
import classes as cl
import bdd_create as bdd

# On importe Tkinter
from tkinter import *

class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=576, **kwargs)
        self.pack(side="top", fill=X)
        #creation d'une liste déroulante
        self.liste = Listbox(fenetre)
        self.liste.pack(side="top", fill=BOTH)
        #On insère ensuite des éléments
        self.liste.insert(0, "1. Quel aliment souhaitez-vous remplacer ?")
        self.liste.insert(1, "2. Retrouver mes aliments substitués.")
        #self.liste.bind('<<ListboxSelect>>', valider)
        self.bouton_valider = Button(fenetre, text= "Valider", command=self.valider)
        self.bouton_valider.pack(side="right")
        

    def valider(self):
        # index = self.liste.curselection()
        
#        if index == 0:
        self.bouton_valider.pack_forget()
        self.liste.delete (0, END)
        self.poll() 
            

            
        

    def poll(self):
        
        message1 = Label(fenetre, text= "Sélectionnez la catégorie.")
        #Les boutons radio
        var_choix = StringVar()

        choix_1 = Radiobutton(fenetre, text="1) Aliments à base de fruits et de légumes", variable=var_choix, value="1")
        choix_2 = Radiobutton(fenetre, text="2) Biscuits apéritifs", variable=var_choix, value="2")
        choix_3 = Radiobutton(fenetre, text="3) Boissons", variable=var_choix, value="3")
        choix_4 = Radiobutton(fenetre, text="4) Bœuf", variable=var_choix, value="4")
        choix_5 = Radiobutton(fenetre, text="5) Chips", variable=var_choix, value="5")
        choix_6 = Radiobutton(fenetre, text="6) Desserts", variable=var_choix, value="6")
        choix_7 = Radiobutton(fenetre, text="7) Fromages", variable=var_choix, value="7")
        choix_8 = Radiobutton(fenetre, text="8)Légumes frais", variable=var_choix, value="8")
        choix_9 = Radiobutton(fenetre, text="9) Pâtisseries", variable=var_choix, value="9")
        choix_10 = Radiobutton(fenetre, text="10) Surgelés", variable=var_choix, value="10")

        choix_1.pack()
        choix_2.pack()
        choix_3.pack()
        choix_4.pack()
        choix_5.pack()
        choix_6.pack()
        choix_7.pack()
        choix_8.pack()
        choix_9.pack()
        choix_10.pack()





        

        


fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()
