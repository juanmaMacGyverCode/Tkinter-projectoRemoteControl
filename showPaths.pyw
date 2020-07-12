from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from tkinter import filedialog


class ShowPaths:

    ############################

    def __init__(self):
        self.title = "Control Panel"
        self.icon = "./Proyectito/imagenes/favicon.ico"
        #self.icon_alt = "./18Tkinter/imagenes/favicon.ico"
        self.size = "500x400"
        self.resizable = True
        self.listNombres = ["XAMPP", "libro1", "libro2", "libro3",
                            "libro4", "libro5", "libro6", "libro7", "libro8", "libro9"]

    def load(self):
        window = Tk()
        self.window = window

        window.title(self.title)
        ruta_icono = os.path.abspath(self.icon)

        #if not os.path.isfile(ruta_icono):
        #    ruta_icono = os.path.abspath(self.icon_alt)

        window.iconbitmap(ruta_icono)
        #window.geometry(self.size)

        if self.resizable:
            window.resizable(1, 1)
        else:
            window.resizable(0, 0)
            
        ############################################################################

        container = Frame(self.window)
        container.config(
            width=500
        )
        canvas = Canvas(container)
        scrollbar = Scrollbar(
            container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        scrollable_frame.config(
            width=500
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        #Abrir conexión
        self.conexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/panel.db')

        #Crear cursor (permite ejecutar consultas)
        self.cursor = self.conexion.cursor()

        self.cursor.execute("SELECT * FROM path;")
        rutas = self.cursor.fetchall()

        for i in range(len(rutas)):
            label = Label(scrollable_frame, text=rutas[i])
            label.pack(anchor=W)

        self.conexion.close()

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    ########################################################################################

       

    ###############################################

    def run(self):
        self.window.mainloop()
