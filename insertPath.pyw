from tkinter import messagebox as MessageBox
import os.path
from tkinter import *
import webbrowser as wb
import math
import sqlite3
from tkinter import filedialog

class InsertForm:

    def __init__(self):
        self.title = "Control remote"
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

        label = Label(self.window, text="Name")
        label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        name = Entry(self.window)
        name.grid(row=1, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        name.config(justify="right", state="normal")

        label = Label(self.window, text="Path")
        label.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        path = Entry(self.window)
        path.grid(row=2, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        path.config(justify="right", state="normal")

        button = Button(self.window, text="Open browser", command=lambda: self.openWindowFileDialog(path))
        button.grid(row=2, column=7)

        opcion = StringVar()
        opcion.set("Red")

        Label(self.window, text="Choose a color").grid(row=3, column=0)

        color = Entry(self.window)
        color.grid(row=3, column=1, columnspan=6, sticky=W, padx=5, pady=5)
        color.config(justify="right", state="readonly")

        select = OptionMenu(self.window, opcion, "Red", "Green", "Blue", "dark orange", "deep pink", "purple", "saddle brown")
        select.grid(row=3, column=7)

        Button(self.window, text="Select", command=lambda: self.seleccionar(opcion, color)).grid(row=3, column=9)
        Button(self.window, text="Save", command=lambda: self.saveNewPath(name.get(), path.get(), color.get())).grid(row=4, column=0)


    def saveNewPath(self, name, path, color):

        if self.isValidatePath(name, path, color):
            self.conexion = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+'/panel.db')
            self.cursor = self.conexion.cursor()
            self.cursor.execute("INSERT INTO path VALUES(null, '" + name + "', '" + path + "', '" + color + "')")
            self.conexion.commit()
            self.conexion.close()
            self.window.destroy()

    def isValidatePath(self, name, path, color) -> bool:
        if len(name) == 0:
            MessageBox.showerror("Error", "The name does not empty")
            return False
        else:
            if len(color) == 0:
                MessageBox.showerror("Error", "The color does not empty")
                return False
            else:
                if len(path) == 0:
                    MessageBox.showerror("Error", "The path does not empty")
                    return False
                else:
                    if not os.path.exists(path):
                        MessageBox.showerror("Error", "The path does not exist")
                        return False

        return True

    def seleccionar(self, opcion, campo):
        campo.config(state="normal")
        campo.delete(0, 20)
        campo.insert(0, opcion.get())
        campo.config(state="readonly")

    def openWindowFileDialog(self, campo):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        campo.insert(0, filename)

    def run(self):
        self.window.mainloop()

