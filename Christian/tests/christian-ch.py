# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import messagebox
import os
import datetime
from utils import Database
from win32api import GetSystemMetrics
import time

# pip install mysql-connector-python

# db = Database()
# db.get_last_details()

devmode = False

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Christian")
        # self.iconbitmap("christian.ico")
        ctk.set_appearance_mode("dark")
        self.attributes('-fullscreen', True)  # Plein écran
        self.attributes('-topmost', True)

        # Empêche la fermeture par la croix
        self.tentatives = 0
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configuration dynamique des éléments
        self.configure_window()

        # Affichage de l'utilisateur de la session
        self.username_label = ctk.CTkLabel(self.container, text=f"Utilisateur: {os.getlogin()}", font=("Calibri", self.font_size(0.02)))
        self.username_label.pack(pady=self.padding(0.03))

        # Affichage en temps réel de la date
        self.time_label = ctk.CTkLabel(self.container, text="Date et heure:", text_color="grey", font=("Calibri", self.font_size(0.02)))
        self.time_label.pack(ipady=self.padding(0.0))
        self.update_time()

        # Label ancien statut
        self.info_label = ctk.CTkLabel(self.container, text="Anciennes remarques", font=("Calibri", self.font_size(0.025)))
        self.info_label.pack(pady=(self.padding(0.02)))
        
        # Ancien statut
        self.last_textbox = ctk.CTkTextbox(self.container, height=self.height_percentage(0.001), width=self.width_percentage(0.4), corner_radius=10, wrap='word')
        self.last_textbox.pack()
        self.last_textbox.insert("0.0", self.get_last())
        self.last_textbox.configure(state="disabled")
        
        # Label remarques
        self.info_label = ctk.CTkLabel(self.container, text="Vos remarques", font=("Calibri", self.font_size(0.025)))
        self.info_label.pack(pady=(self.padding(0.02)))
        
        # Zone à remplir
        self.info_textbox = ctk.CTkTextbox(self.container, height=self.height_percentage(0.15), width=self.width_percentage(0.4), corner_radius=10, wrap='word')
        self.info_textbox.pack(padx=self.padding(0.025))

        # Checkboxes
        self.prof_checkbox = ctk.CTkCheckBox(self.container, text="Vu par le professeur", width=self.width_percentage(0.15), command=self.vuprof)
        self.prof_checkbox.pack(pady=self.padding(0.03), side = 'left', padx=self.padding(0.025))
    
        # Bouton valider
        self.close_button = ctk.CTkButton(self.container, text="Valider", width=self.width_percentage(0.07), command=self.close_app)
        self.close_button.pack(pady=self.padding(0.03), side = 'right', padx=self.padding(0.025))

    def configure_window(self):
        """Ajuste la taille et la position de la fenêtre selon la résolution de l'écran."""
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

        # Taille dynamique pour le conteneur
        container_width = int(self.screen_width * 0.6)
        container_height = int(self.screen_height * 0.4)

        # Positionnement centré
        self.container = ctk.CTkFrame(self, width=container_width, height=container_height, corner_radius=15)
        self.container.place(relx=0.5, rely=0.5, anchor="center")  # Centrage avec anchor
    
    def font_size(self, fraction):
        """Calcul la taille de la police en fonction de la hauteur de l'écran."""
        return int(self.screen_height * fraction)

    def width_percentage(self, fraction):
        """Calcul la largeur en pourcentage de l'écran."""
        return int(self.screen_width * fraction)

    def height_percentage(self, fraction):
        """Calcul la hauteur en pourcentage de l'écran."""
        return int(self.screen_height * fraction)

    def padding(self, fraction):
        """Calcul le padding en fonction de la hauteur de l'écran."""
        return int(self.screen_height * fraction)

    def update_time(self):
        """Met à jour l'heure affichée en temps réel."""
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.configure(text=f"Date et heure: {current_time}")
        self.after(1000, self.update_time)  # Mise à jour toutes les secondes

    def vuprof(self):
        if devmode:
            self.destroy()
        else:
            print(self.prof_checkbox.get())
        
    def on_closing(self):
        self.tentatives += 1
        messagebox.showwarning("Avertissement", "Vous n'avez pas le droit de quitter l'application. Il ne vous reste plus que " + str(4 - self.tentatives) + " tentatives avant votre exclusion définitive du lycée.")
        if self.tentatives > 3:
            os.system('shutdown -s -t 1')

    def close_app(self):
        os.system("start explorer.exe")
        db = Database()
        db.insert(self.info_textbox.get("0.0", "end"))
        self.destroy()
        
    def get_last(self):
        db = Database()
        return db.get_last_details()

if __name__ == "__main__":
    os.system("taskkill -f -im explorer.exe")
    app = App()
    app.mainloop()