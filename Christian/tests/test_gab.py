import customtkinter as ctk
from tkinter import messagebox
import os
import datetime
from utils import Database
from win32api import GetSystemMetrics

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

        # Zone de remarques
        self.info_label = ctk.CTkLabel(self.container, text="Remarques", font=("Calibri", self.font_size(0.025)))
        self.info_label.pack(pady=(self.padding(0.02)))

        self.info_textbox = ctk.CTkTextbox(self.container, height=self.height_percentage(0.15), width=self.width_percentage(0.4), corner_radius=10)
        self.info_textbox.pack(padx=self.padding(0.025))

        # Checkboxes
        self.prof_checkbox = ctk.CTkCheckBox(self.container, text="Vu par le professeur", width=self.width_percentage(0.15))
        self.prof_checkbox.pack(pady=self.padding(0.03), side='left', padx=self.padding(0.025))
        
        self.close_checkbox = ctk.CTkButton(self.container, text="Valider les dires", width=self.width_percentage(0.1), command=self.close_app)
        self.close_checkbox.pack(pady=self.padding(0.03), side='right', padx=self.padding(0.025))

        # Bloquer la touche Tab
        self.bind("<Tab>", self.block_tab)

    def block_tab(self, event):
        """Bloque l'événement de la touche Tab."""
        return "break"  # Empêche le comportement par défaut de la touche Tab

    def configure_window(self):
        """Ajuste la taille et la position de la fenêtre selon la résolution de l'écran."""
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

        # Taille dynamique pour le conteneur
        container_width = int(self.screen_width * 0.6)
        container_height = int(self.screen_height * 0.4)

        # Vérification des dimensions (débogage)
        print(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
        print(f"Container dimensions: {container_width}x{container_height}")

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
        self.after()