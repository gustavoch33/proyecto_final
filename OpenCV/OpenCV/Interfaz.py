from tkinter import *
from tkinter import ttk

root = Tk()

root.title("INTERFAZ") #Inserta titulo a la ventana
root.resizable(False, False) #Bloque la ventana y no permite expandirla
#root.iconbitmap("icono.ico") #Cambiamos el icono de la ventana
root.geometry("400x200") #Cambiamos las dimensiones de la ventana
#root.config(bg = "green") #Configura los valores esteticos de la ventana

frm = Frame(root) #Se crea un frame donde insertaremos los widgets
frm.pack()
frm.grid_rowconfigure(1, weight=1)
frm.grid_rowconfigure(2, weight=1)
frm.grid_columnconfigure(1, weight=1)
#frm.config(bg = "green")

puerto = Label(frm, text = "Puerto:")
puerto.grid(column = 0, row = 0, sticky = "e", padx = 10, pady = 10)

ms = Entry(frm)
ms.grid(column = 1, row = 0, padx = 10, pady = 10)

tb = ttk.Combobox(frm, state = "readonly")
tb.grid(column = 0, row = 2)

button1 = Button(frm, text = "Mostrar", command = lambda:imprimir())
button1.grid(column = 1, row = 3)

def imprimir():
    if ms.get() == "":
        pass
    else:
        options = list(tb['values'])
        tb['values'] = options + [str(ms.get())]

button2 = Button(frm, text = "Salir", command = root.destroy)
button2.grid(column = 0, row = 5)

root.mainloop()