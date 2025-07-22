import serial, time
from tkinter import *

root = Tk()
root.title("INTERFAZ") #Inserta titulo a la ventana
root.resizable(False, False) #Bloque la ventana y no permite expandirla
root.geometry("200x100") #Cambiamos las dimensiones de la ventana

frm = Frame(root) #Se crea un frame donde insertaremos los widgets
frm.pack()
frm.grid_rowconfigure(1, weight=1)
frm.grid_rowconfigure(2, weight=1)
frm.grid_columnconfigure(1, weight=1)

serialCOM = serial.Serial("COM5", 9600)

led1 = Button(frm, text = "Encender Led 1", command = lambda:encenderLed1())
led1.grid(column = 0, row = 0, padx = 10, pady = 10)

led1 = Button(frm, text = "Encender Led 1", command = lambda:encenderLed1())
led1.grid(column = 0, row = 0, padx = 10, pady = 10)

def encenderLed1():
    ms = "M"

    serialCOM.write(ms.encode('utf-8'))

root.mainloop()

#while True:
#    ms = input("Escriba una letra: ").upper()

#    serialCOM.write(ms.encode('utf-8'))

#    time.sleep(0.5)

#    conf = str(serialCOM.read().decode('utf-8'))
#    print(conf)

