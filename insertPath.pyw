from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from tkinter import filedialog

class InsertForm:

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

        #################################

        #Label
        label = Label(self.window, text="Name")
        label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        #Campo de texto
        name = Entry(self.window)
        name.grid(row=1, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        name.config(justify="right", state="normal")

        #Label
        label = Label(self.window, text="Path")
        label.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        #Campo de texto
        path = Entry(self.window)
        path.grid(row=2, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        path.config(justify="right", state="normal")

        #Button para escoger fichero
        button = Button(self.window, text="Open browser", command=lambda: self.openWindowFileDialog(path))
        button.grid(row=2, column=7)

        ## Menú
        #def seleccionar():
            #seleccionado.config(text=opcion.get())

        opcion = StringVar()
        opcion.set("Red")

        Label(self.window, text="Choose a color").grid(row=3, column=0)

        #Campo de texto
        color = Entry(self.window)
        color.grid(row=3, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        color.config(justify="right", state="readonly")

        select = OptionMenu(self.window, opcion, "Red", "Green", "Blue", "dark orange", "deep pink", "purple", "saddle brown")
        select.grid(row=3, column=7)

        Button(self.window, text="Select", command=lambda: self.seleccionar(opcion, color)).grid(row=3, column=9)


        Button(self.window, text="Save", command=lambda: self.saveNewPath(name.get(), path.get(), color.get())).grid(row=4, column=0)


    def saveNewPath(self, name, path, color):

        #Abrir conexión
        self.conexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/panel.db')
        #Crear cursor (permite ejecutar consultas)
        self.cursor = self.conexion.cursor()

        # Insertar datos
        self.cursor.execute("INSERT INTO path VALUES(null, '" + name + "', '" + path + "', '" + color + "')")
        self.conexion.commit()


        self.conexion.close()

        self.window.destroy()

    def seleccionar(self, opcion, campo):
        campo.config(state="normal")
        campo.delete(0, 20)
        campo.insert(0, opcion.get())
        campo.config(state="readonly")

    def openWindowFileDialog(self, campo):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        campo.insert(0, filename)

    ###############################################

    def run(self):
        self.window.mainloop()

