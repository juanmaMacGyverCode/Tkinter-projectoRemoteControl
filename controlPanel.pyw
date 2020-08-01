from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from insertPath import InsertForm
from showPaths import ShowPaths

class ControlRemote:

    def __init__(self):
        self.title = "Control remote"
        self.icon = "./imagenes/logo.ico"
        self.size = "300x300"
        self.resizable = True

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

        window.iconbitmap(ruta_icono)

        if self.resizable:
            window.resizable(1, 1)
        else:
            window.resizable(0, 0)

        mi_menu = Menu(self.window)
        self.window.config(menu=mi_menu)

        archivo = Menu(mi_menu, tearoff=0)
        archivo.add_command(label="New path", command=self.createWindowFormPath)
        archivo.add_command(label="Show paths", command=self.showPaths)
        archivo.add_separator()
        archivo.add_command(label="Exit", command=self.window.quit)

        mi_menu.add_cascade(label="File", menu=archivo)
        mi_menu.add_command(label="Refresh", command=self.refresh)

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

        button = Button(marco, text="Delete", command=lambda: self.deletePath(id))
        button.pack(side=LEFT)
        button = Button(marco, text="Abrir", command=lambda: self.openFile(ruta))
        button.pack(side=RIGHT)
    
    def deletePath(self, idPath):

        self.conexion = sqlite3.connect(os.path.dirname(
            os.path.abspath(__file__))+'/panel.db')
        self.cursor = self.conexion.cursor()

        self.cursor.execute("SELECT * FROM path;")
        paths = self.cursor.fetchall()

        errors = True

        for path in paths:
            if int(path[0]) == int(idPath):
                self.cursor.execute(
                    "DELETE FROM path WHERE id ='" + str(idPath) + "';")
                self.conexion.commit()
                errors = False

        if errors:
            MessageBox.showerror(
                "Error", "The identificator path does not exist or it's not a number")

        self.conexion.close()

        self.refresh()

    def refresh(self):
        self.window.destroy()
        
        newWindow = ControlRemote()
        newWindow.load()
        newWindow.run()

    def createWindowFormPath(self):
        insertForm = InsertForm()
        insertForm.load()

        insertForm.run()

    def openFile(self, ruta):
        if os.path.exists(ruta):
            wb.open_new(ruta)
        else:
            MessageBox.showerror("Error", "The path does not exist")

    def run(self):
        self.window.mainloop()


program = ControlRemote()
program.load()
program.run()
