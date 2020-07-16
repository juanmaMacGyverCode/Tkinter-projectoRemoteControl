from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from insertPath import InsertForm
from showPaths import ShowPaths
from deletePath import DeletePath

class Programa:

    ############################

    def __init__(self):
        self.title = "Control Panel"
        self.icon = "./imagenes/favicon.ico"
        self.icon_alt = "./Proyectito/imagenes/favicon.ico"
        self.size = "300x300"
        self.resizable = True
        self.listNombres = ["XAMPP", "libro1", "libro2", "libro3",
                            "libro4", "libro5", "libro6", "libro7", "libro8", "libro9"]

        self.conexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/panel.db')
        self.cursor = self.conexion.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS path(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre VARCHAR(20),
               direccion VARCHAR(200),
               grupo VARCHAR(20)
               )""")

        self.conexion.commit()

        self.conexion.close()

    def load(self):
        window = Tk()
        self.window = window

        window.title(self.title)
        ruta_icono = os.path.abspath(self.icon)
        #ruta_icono = os.path.relpath(self.icon)
        #ruta_icono = self.icon

        window.iconbitmap(ruta_icono)

        if self.resizable:
            window.resizable(1, 1)
        else:
            window.resizable(0, 0)

        #######################################################################################################################################

        mi_menu = Menu(self.window)
        self.window.config(menu=mi_menu)

        # MENÚ DE LA APLICACIÓN
        # El tearoff es para quitar las lineas separadoras del menu y solo dejar las que yo quiero
        archivo = Menu(mi_menu, tearoff=0)
        archivo.add_command(label="New path", command=self.nuevaVentana)
        archivo.add_command(label="Delete path", command=self.deletePath)
        archivo.add_separator()
        archivo.add_command(label="Show paths", command=self.showPaths)
        archivo.add_command(label="Abrir carpeta")
        archivo.add_separator()
        archivo.add_command(label="Salir", command=self.window.quit)

        mi_menu.add_cascade(label="Archivo", menu=archivo)
        mi_menu.add_command(label="Editar")
        mi_menu.add_command(label="Refresh", command=self.refresh)

        ##########################################################################################################################################

        container = Frame(self.window)
        container.config(
            width=500
        )
        canvas = Canvas(container)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
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

        self.conexion = sqlite3.connect(os.path.dirname(
            os.path.abspath(__file__))+'/panel.db')

        self.cursor = self.conexion.cursor()

        self.cursor.execute("SELECT * FROM path;")
        self.listNombres = self.cursor.fetchall()

        self.conexion.close()

        self.listaIndices = []

        for i in range(math.ceil(len(self.listNombres)/3)):
            for j in range(3):
                if (1+2*i)+i+j <= len(self.listNombres):
                    self.createBoxButton(i, j, self.listNombres[(1+2*i)+i+j - 1][0], self.listNombres[(1+2*i)+i+j - 1][1], self.listNombres[(1+2*i)+i+j - 1][2], self.listNombres[(1+2*i)+i+j - 1][3], scrollable_frame)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def deletePath(self):
        newWindow = DeletePath()
        newWindow.load()
        newWindow.run()

    def showPaths(self):
        newWindow = ShowPaths()
        newWindow.load()
        newWindow.run()

    def createBoxButton(self, i, j, id, nombre, ruta, color, scrollable_frame):

        marco = Frame(scrollable_frame, width=126, height=100)
        marco.config(
            bg=color,
            bd=5,
            relief="raised"
        )

        marco.grid(row=i, column=j % 3)
        marco.pack_propagate(False)

        texto = Label(marco, text=id)
        texto.config(
            bg=color,
            fg="white",
            font=("Arial", 12)
        )
        texto.pack(anchor=CENTER, fill=Y, expand=YES)
        texto = Label(marco, text=nombre)
        texto.config(
            bg=color,
            fg="white",
            font=("Arial", 12)
        )
        texto.pack(anchor=CENTER, fill=Y, expand=YES)

        button = Button(marco, text="Abrir", command=lambda: self.abrir(ruta))
        button.pack(anchor=CENTER)

    def refresh(self):
        self.window.destroy()
        
        newWindow = Programa()
        newWindow.load()
        newWindow.run()

    def nuevaVentana(self):
        #ventana = Tk()
        insertForm = InsertForm()
        insertForm.load()

        insertForm.run()
        #ventana.mainloop()

    def abrir(self, ruta):
        if os.path.exists(ruta):
            wb.open_new(ruta)
        else:
            MessageBox.showerror("Error", "The path does not exist")

    ###############################################

    def run(self):
        self.window.mainloop()


programa = Programa()
programa.load()
programa.run()
