from tkinter import *
from PIL import Image, ImageTk
import random


valeur_compteur = 0  # Besoin de la définir ici sinon erreur undefined
buttons = []  # Liste contenant les images
checkifwon = []
melange_fait = False


def echanger_canvas(index1, index2, buttons):
    """
    Cette fonction échange visuellement deux canvas sur la grille.
    Elle met également à jour le compteur de coups et vérifie si le jeu est gagné.

    Paramètres :
    index1 (int) : Index du premier canvas à échanger (case cliquée)
    index2 (int) : Index du deuxième canvas à échanger (case grise)
    buttons (list) : Liste des canvases à échanger

    Retourne :
    None
    """
    # Echange visuel des canva
    canvas1 = buttons[index1]
    canvas2 = buttons[index2]
    ligne1, colonne1 = canvas1.grid_info()["row"], canvas1.grid_info()["column"]
    ligne2, colonne2 = canvas2.grid_info()["row"], canvas2.grid_info()["column"]
    canvas1.grid(row=ligne2, column=colonne2)
    canvas2.grid(row=ligne1, column=colonne1)

    # Lié compteur nb de coups
    global valeur_compteur
    valeur_compteur = valeur_compteur + 1
    compteur_label.config(text=valeur_compteur)
    if buttons == checkifwon:
        window = Tk()
        window.geometry("300x100")
        window.title("Jeu de taquin")
        label = Label(window, text="Félicitations! :-)", font=("Arial", 16))
        label.pack(pady=20)
        window.mainloop()


def quand_cliquee(original_index, buttons):
    """
    Cette fonction est appelée lorsque l'utilisateur clique sur un bouton.
    Elle vérifie si le bouton cliqué peut être échangé avec le bouton en gris.

    Paramètres :
    original_index (int) : Index du bouton sur lequel l'utilisateur a cliqué
    buttons (list) : Liste des canvas du jeu

    Retourne :
    original_index (int)
    index_gris (int)
    buttons (list)
    """
    index_gris = next((i for i, button in enumerate(buttons) if button.index == 15), None)
    canvas_gris = buttons[index_gris]
    canvas_original = buttons[original_index]
    ligne_gris, colonne_gris = canvas_gris.grid_info()["row"], canvas_gris.grid_info()["column"]
    ligne_original, colonne_original = canvas_original.grid_info()["row"], canvas_original.grid_info()["column"]
    # Vérification possibilité échange par emplacement sur la grille plutôt que par index, car les index ne changent jamais (sinon comment savoir qui est le gris ???)
    if ((ligne_original == ligne_gris + 1 or ligne_original == ligne_gris - 1) and colonne_original == colonne_gris) or ((colonne_original == colonne_gris + 1 or colonne_original == colonne_gris - 1) and ligne_original == ligne_gris):
        if melange_fait:
            echanger_canvas(original_index, index_gris, buttons)


def taquin_game(image_path):
    """
    Cette fonction est lancé au démarrage du programme, elle
    crée la fenetre tkinter et le canva utilisé pour afficher l'image

    Paramètres :
    image_path(str) : Chemin d'accès de l'image utilisée

    Retourne :
    None
    """
    window = Tk()

    # Les 5 lignes suivantes servent à process le nécessaire pour la fenetre Tk et l'image
    image_choisie = Image.open(image_path)  # Sert à charger l'image voulue
    original_width, original_height = image_choisie.size  # Nécessaire pour pouvoir calculer le ratio de l'image
    half_largeur_ecran = window.winfo_screenwidth() // 2  # Utile pour définir la taille de la fenetre Tk et le ratio de l'image
    hauteur_resize_souhait = int(half_largeur_ecran * original_height / original_width)  # Pour resize l'image
    image_resized = image_choisie.resize((int(half_largeur_ecran), int(hauteur_resize_souhait)))

    # Les 3 lignes suivantes servent à définir les caractéristiques de la fenetre Tk
    window.geometry(f"{half_largeur_ecran + 100}x{hauteur_resize_souhait +25}")
    window.title("Jeu de Taquin")
    window.resizable(False, False)  # Evite divers bugs d'affichage

    converted_for_canva_image = ImageTk.PhotoImage(image_resized)  # Nécessaire pour pouvoir afficher l'image
    # Crée une grille de boutons de 4x4 de la taille voulue
    indextest = -1
    for ligne in range(4):
        for colonne in range(4):
            # Crée un canva
            canvas_image = Canvas(window, width=half_largeur_ecran // 4, height=hauteur_resize_souhait // 4)
            canvas_image.create_image(-colonne * (half_largeur_ecran // 4), -ligne * (hauteur_resize_souhait // 4), image=converted_for_canva_image, anchor='nw')
            canvas_image.grid(row=ligne, column=colonne)
            buttons.append(canvas_image)
            checkifwon.append(canvas_image)
            canvas_image.index = len(buttons) - 1  # Ajoute l'attribut index à chaque canvas
            # Ajoute la liaison de l'événement de clic à chaque canvas
            indextest = indextest + 1
            canvas_image.bind("<Button-1>", lambda event, index=indextest: quand_cliquee(original_index, buttons))

    # Les 2 lignes suivantes sont nécessaires pour enlever un des "carreaux"
    last_canvas = buttons[-1]
    last_canvas.create_rectangle(0, 0, half_largeur_ecran // 4, hauteur_resize_souhait // 4, fill="dark grey", outline="dark grey")
    original_index = buttons[:]

    # Les lignes suivantes sont necessaires pour mélanger les pieces et mettre un bouton permettant de le faire

    def melanger_pieces():
        """
        Cette fonction est appelée lorsque l'utilisateur clique sur le bouton mélanger, elle mélange les éléments
        du canva puis recalcule leurs index

        Paramètres :
        None

        Retourne :
        index_canva_gris
        """
        random.shuffle(buttons)
        for elem, mesimages in enumerate(buttons):  # Usage d'enumerate pour recuperer l'index et la valeur de chaque element en simultanee
            ligne_melange = elem // 4
            colonne_melange = elem % 4
            mesimages.grid(row=ligne_melange, column=colonne_melange)
            buttons[elem] = mesimages
            global melange_fait
            melange_fait = True
            mesimages.bind("<Button-1>", lambda event, index=elem: quand_cliquee(index, buttons))
            global valeur_compteur
            valeur_compteur = 0
            compteur_label.config(text=valeur_compteur)
            assert valeur_compteur >=0


    # Bouton mélanger
    bouton_melanger = Button(window, text="Mélanger", command=melanger_pieces)
    bouton_melanger.grid(row=0, column=4, rowspan=4, padx=10)

    # Compteur du nombre de coups
    global compteur_label
    compteur_label = Label(window, text=str(valeur_compteur), font="courrier 20 bold")
    compteur_label.grid(row=0, column=4, rowspan=3, padx=10)

    window.mainloop()


# Pour tester, modifier le chemin d'accès si vous souhaitez une autre image
taquin_game("eiffer_tower.jpg")
