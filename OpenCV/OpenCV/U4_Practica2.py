from tkinter import *
from tkinter import ttk as tk
from tkinter import messagebox
import serial
import collections
from time import sleep

serialCOM = serial.Serial()
serialCOM.baudrate = 9600

root = Tk()
root.title("INTERFAZ") #Inserta titulo a la ventana
root.resizable(False, False) #Bloque la ventana y no permite expandirla
root.geometry("600x200") #Cambiamos las dimensiones de la ventana

#  Obtenemos el largo y  ancho de la pantalla
wtotal = root.winfo_screenwidth()
htotal = root.winfo_screenheight()
#  Guardamos el largo y alto de la ventana
wventana = 600
hventana = 200

#  Aplicamos la siguiente formula para calcular donde debería posicionarse
pwidth = round(wtotal/2-wventana/2)
pheight = round(htotal/2-hventana/2)

#  Se lo aplicamos a la geometría de la ventana
root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

frm = Frame(root) #Se crea un frame donde insertaremos los widgets
frm.pack()
frm.grid_rowconfigure(1, weight=1)
frm.grid_rowconfigure(2, weight=1)
frm.grid_columnconfigure(1, weight=1)

txt1 = Label(frm, text = "Puerto:")
txt1.grid(column = 0, row = 0, sticky = "e", padx = 10, pady = 10)

puertos = tk.Combobox(frm, state = "readonly")
puertos.grid(column = 1, row = 0, padx = 10, pady = 10)

buscar = Button(frm, text = "Buscar", command = lambda:buscarPuertos(), width = 16, height = 2)
buscar.grid(column = 1, row = 1, padx = 10, pady = 10)

def buscarPuertos():
    ports = ['COM%s' % (i + 1) for i in range(256)]
    encontrados = []
    for port in ports:
        try:
            serialCOM = serial.Serial(port)
            serialCOM.close()
            encontrados.append(port)
        except (OSError, serial.SerialException):
            pass

    if len(encontrados) > 0 :
        puertos["values"] = encontrados
        puertos.current(0)
        con["state"] = "normal"
    else:
        messagebox.showinfo(title="INFO", message="No se encontrarion puertos")
        con["state"] = "disable"

con = Button(frm, text = "Conectar", command = lambda:conexion(), state = "disable", width = 16, height = 2)
con.grid(column = 0, row = 1, padx = 10, pady = 10)

def conexion():
    try:
        if con["text"] == "Conectar":
            serialCOM.port = str(puertos.get())
            serialCOM.open()
            con["text"] = "Desconectar"
            foco1["state"] = "normal"
            foco2["state"] = "normal"
        else:
            serialCOM.close()
            con["text"] = "Conectar"
            foco1["state"] = "disable"
            foco2["state"] = "disable"
    except (OSError, serial.SerialException):
            pass

foco1 = Button(frm, text = "Foco 1", command = lambda:encender1(), state = "disable", width = 16, height = 2)
foco1.grid(column = 0, row = 2, padx = 10, pady = 10)

def encender1():
    if serialCOM.is_open == True:
        ms = "C"    
        serialCOM.write(ms.encode('utf-8'))
        sleep(1)
        ms = "R"    
        serialCOM.write(ms.encode('utf-8'))
    else:
        pass

foco2 = Button(frm, text = "Foco 2", command = lambda:encender2(), state = "disable", width = 16, height = 2)
foco2.grid(column = 1, row = 2, padx = 10, pady = 10)

def encender2():
    if serialCOM.is_open == True:
        ms = "B"    
        serialCOM.write(ms.encode('utf-8'))
        sleep(1)
        ms = "R"    
        serialCOM.write(ms.encode('utf-8'))
    else:
        pass

txt1 = Label(frm, text = "Valor Pote:")
txt1.grid(column = 2, row = 0, sticky = "S", padx = 10, pady = 10)

adc = Entry(frm, state = "readonly")
adc.grid(column = 2, row = 1, padx = 10, pady = 10)

root.mainloop()