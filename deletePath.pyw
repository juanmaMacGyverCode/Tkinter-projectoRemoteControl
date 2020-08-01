from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from tkinter import filedialog

class DeletePath:

    def __init__(self):
        self.title = "Control Panel"
        self.icon = "./imagenes/logo.ico"
        self.size = "500x400"
        self.resizable = True

    def load(self):
        window = Tk()
        self.window = window

        window.title(self.title)
        ruta_icono = os.path.abspath(self.icon)

        window.iconbitmap(ruta_icono)

        if self.resizable:
            window.resizable(1, 1)
        else:
            window.resizable(0, 0)

        label = Label(self.window, text="Identificator(ej: 1)")
        label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        entryDeletePath = Entry(self.window)
        entryDeletePath.grid(row=1, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        entryDeletePath.config(justify="right", state="normal")

        Button(self.window, text="Save", command=lambda: self.deletePath(entryDeletePath.get())).grid(row=4, column=0)

    def deletePath(self, idPath):

        self.conexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/panel.db')
        self.cursor = self.conexion.cursor()

        self.cursor.execute("SELECT * FROM path;")
        paths = self.cursor.fetchall()

        errors = True

        for path in paths:
            if idPath.isnumeric():
                if int(path[0]) == int(idPath):
                    self.cursor.execute("DELETE FROM path WHERE id ='" + idPath + "';")
                    self.conexion.commit()
                    errors = False

        if errors:
            MessageBox.showerror("Error", "The identificator path does not exist or it's not a number")
        
        self.conexion.close()

        self.window.destroy()

    def seleccionar(self, opcion, campo):
        campo.config(state="normal")
        campo.delete(0, 20)
        campo.insert(0, opcion.get())
        campo.config(state="readonly")

    def openWindowFileDialog(self, campo):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file")
        campo.insert(0, filename)

    def run(self):
        self.window.mainloop()
