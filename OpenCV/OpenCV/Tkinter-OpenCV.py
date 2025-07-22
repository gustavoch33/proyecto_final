from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
from threading import Thread, Event
from time import sleep

x1, y1 = 190, 80
x2, y2 = 450, 398

global countP
global countN
countP = 775
countN = 600

global datoP
datoP = "p"
if not os.path.exists(datoP):
    print("Carpeta creada: ", datoP)
    os.makedirs(datoP)

global datoN
datoN = "n"
if not os.path.exists(datoN):
    print("Carpeta creada: ", datoN)
    os.makedirs(datoN)

def visualizar():
    global cap
    if cap is not None:
        global ret, frame
        global objeto
        ret, frame = cap.read()
        if ret == True:
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 1)

            imAux = frame.copy()
            objeto = imAux[y1:y2,x1:x2]
            objeto = imutils.resize(objeto, width = 38)

            frame = imutils.resize(frame, width = 640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image = im)

            mVideo.configure(image = img)
            mVideo.image = img
            mVideo.after(10, visualizar)

            cv2.imshow("objeto", objeto)

            #Tres comillas comenta varias lineas
            """global hilo
            global señal

            señal = Event()
            hilo = Thread(target = inVideo)
            señal.set()
            hilo.start()
            """

        else:
            mVideo.image = ""
            cap.release()

def iniciar():
    global cap
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    visualizar()

def finalizar():
    """global hilo
    global señal

    if hilo is not None:
        señal.clear()
        hilo.join()
        hilo = None
        print("Hilo desactivado")"""


    global cap
    cap.release()

def saveP():
    global ret
    if ret == True:
        global countP
        global objeto
        cv2.imwrite(datoP + "/objeto_{}.jpg".format(countP), objeto)
        print("Imagen almacenada: ", "objeto_{}.jpg".format(countP))
        countP += 1

def saveN():
    global ret
    if ret == True:
        global countN
        global objeto
        cv2.imwrite(datoN + "/objeto_{}.jpg".format(countN), objeto)
        print("Imagen almacenada: ", "objeto_{}.jpg".format(countN))
        countN += 1

cap = None
root = Tk()

root.title("INTERFAZ") #Inserta titulo a la ventana
root.resizable(False, False) #Bloque la ventana y no permite expandirla
root.geometry("700x600") #Cambiamos las dimensiones de la ventana

#  Obtenemos el largo y  ancho de la pantalla
wtotal = root.winfo_screenwidth()
htotal = root.winfo_screenheight()
#  Guardamos el largo y alto de la ventana
wventana = 700
hventana = 600

#  Aplicamos la siguiente formula para calcular donde debería posicionarse
pwidth = round(wtotal/2-wventana/2)
pheight = round(htotal/2-hventana/2)

#  Se lo aplicamos a la geometría de la ventana
root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

frm = Frame(root) #Se crea un frame donde insertaremos los widgets
frm.pack()
frm.grid_rowconfigure(0, weight=1)
frm.grid_rowconfigure(1, weight=1)
frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)

btInicar = Button(frm, text = "Iniciar", width = 25, command = iniciar)
btInicar.grid(column = 0, row = 0, padx = 10, pady = 10)

btFinalizar = Button(frm, text = "Finalizar", width = 25, command = finalizar)
btFinalizar.grid(column = 1, row = 0, padx = 10, pady = 10)

mVideo = Label(frm, text = "¡El video se mostrara aquí!")
mVideo.grid(column = 0, row = 1, columnspan = 2, padx = 10, pady = 10)

btSaveP = Button(frm, text = "Save P", width = 25, command = saveP)
btSaveP.grid(column = 0, row = 3, padx = 10, pady = 10)

btSaveN = Button(frm, text = "Save N", width = 25, command = saveN)
btSaveN.grid(column = 1, row = 3, padx = 10, pady = 10)

root.mainloop()
