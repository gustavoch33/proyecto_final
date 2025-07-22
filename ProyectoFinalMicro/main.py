from tkinter import *
from time import sleep
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from comunicacion import Comunicacion
import collections
from PIL import ImageTk, Image
from PIL import ImageTk
import cv2 as cv
import imutils
import os
from threading import Thread, Event
import numpy as np
import time




class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__( master, *args)

        self.datos_pic = Comunicacion()
        self.tm = 0
        self.tiempo = 0
        self.areaVT = 0
        self.areaMT = 0
        self.countdown = None

        self.widgets()



    def hilo(self):
        self.tiempo
        self.countdown

        for i in range(8):
            self.tiempo = self.tiempo - 1
            sleep(1)
            print(self.tiempo)

            if self.tiempo == 5:
                self.foto()
        
            if self.tiempo == 4:
                dato = "R"
                self.datos_pic.enviar_datos(dato)
                print("Retirar")

        print("Tiempo finalizado\n")




    def iniciar(self):
        if (self.cb_port.get() != ""):
            self.datos_pic.pic.port = self.cb_port.get()
            self.datos_pic.pic.baudrate = self.cb_baud.get()
            self.datos_pic.conexion_serial()

            sleep(2)

            self.cap = cv.VideoCapture(int(self.cb_cameras.get()), cv.CAP_DSHOW)

            self.bt_conectar.config(state = "disable")
            self.cb_cameras.config(state = "disable")
            self.cb_port.config(state = "disable")
            self.cb_baud.config(state = "disable")

            self.bt_desconectar.config(state = "normal")
            self.vB.config(state = "normal")
            self.vA.config(state = "normal")
            self.mB.config(state = "normal")
            self.mA.config(state = "normal")
            self.sB.config(state = "normal")
            self.sA.config(state = "normal")
            self.bB.config(state = "normal")
            self.bA.config(state = "normal")

            self.visualizar()

        else:
            messagebox.showinfo(title="INFO", message="¡No hay puertos existentes!")




    def pausar(self):
        self.datos_pic.desconectar()

        self.bt_conectar.config(state = "normal")
        self.cb_cameras.config(state = "normal")
        self.cb_port.config(state = "normal")
        self.cb_baud.config(state = "normal")

        self.bt_desconectar.config(state = "disable")
        self.vB.config(state = "disable")
        self.vA.config(state = "disable")
        self.mB.config(state = "disable")
        self.mA.config(state = "disable")
        self.sB.config(state = "disable")
        self.sA.config(state = "disable")
        self.bB.config(state = "disable")
        self.bA.config(state = "disable")
        self.cap.release()
        cv.destroyAllWindows()




    def reanudar(self):
        self.ani.event_source.start()




    def visualizar(self):
        if self.cap is not None:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # if frame is read correctly ret is True
            if ret == True:
                # Our operations on the frame come here
                imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

                #Verde
                verdeBajo = np.array([self.vB.get(),
                                      self.sB.get(),
                                      self.bB.get()], np.uint8)
                verdeAlto = np.array([self.vA.get(),
                                      self.sA.get(),
                                      self.bA.get()], np.uint8)
                mascaraV = cv.inRange(imghsv, verdeBajo, verdeAlto)

                #Madura
                maduraBajo = np.array([self.mB.get(),
                                       self.sB.get(),
                                       self.bB.get()], np.uint8)
                maduraAlto = np.array([self.mA.get(),
                                       self.sA.get(),
                                       self.bA.get()], np.uint8)
                mascaraM = cv.inRange(imghsv, maduraBajo, maduraAlto)

                #Mascara tamaño
                tamBajo = np.array([self.mB.get(),
                                       self.sB.get(),
                                       self.bB.get()], np.uint8)
                tamAlto = np.array([self.vA.get(),
                                       self.sA.get(),
                                       self.bA.get()], np.uint8)
                mascaraT = cv.inRange(imghsv, tamBajo, tamAlto)

                contornosV, _ =cv.findContours(mascaraV, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                contornosM, _ =cv.findContours(mascaraM, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                contornosT, _ =cv.findContours(mascaraT, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                for c in contornosV:
                    areaV = cv.contourArea(c)
                    self.areaVT = areaV

                    if (areaV > 10000 and areaV <= 36000): #Verde Chica
                        #print("Verde Chica Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                        cv.putText(frame, "Area: " + str(areaV), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        cv.putText(frame, "Guayaba Verde Chica", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()

                    if (areaV > 36000 and areaV <= 52000): #Verde Mediana
                        #print("Verde Mediana Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                        cv.putText(frame, "Area: " + str(areaV), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        cv.putText(frame, "Guayaba Verde Mediana", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()

                    if (areaV > 52000 and areaV <= 80000): #Verde Grande
                        #print("Verde Grande Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                        cv.putText(frame, "Area: " + str(areaV), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        cv.putText(frame, "Guayaba Verde Grande", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()


                for c in contornosM:
                    areaM = cv.contourArea(c)
                    self.areaMT = areaM

                    if (areaM > 10000 and areaM <= 36000): #Madura Chica
                        #print("Madura Chica Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 2)
                        cv.putText(frame, "Area: " + str(areaM), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        cv.putText(frame, "Guayaba Madura Chica", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()

                    if (areaM > 36000 and areaM <= 52000): #Madura Mediana
                        #print("Madura Mediana Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 2)
                        cv.putText(frame, "Area: " + str(areaM), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        cv.putText(frame, "Guayaba Madura Mediana", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()

                    if (areaM > 52000 and areaM <= 80000): #Madura Chica
                        #print("Madura Grande Detectada")
                        detect = True
                        x, y, w, h = cv.boundingRect(c)
                        cv.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 2)
                        cv.putText(frame, "Area: " + str(areaM), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        cv.putText(frame, "Guayaba Madura Grande", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                        if self.tiempo == 0:
                            print("Hilo Iniciado")
                            self.tiempo = 8
                            self.countdown = Thread(target = self.hilo)
                            self.countdown.start()

                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                frame = imutils.resize(frame, width = 300)
                # Display the resulting frame
                im1 = Image.fromarray(frame)
                img1 = ImageTk.PhotoImage(image = im1)

                self.mVideo1.config(bg = "gray50")
                self.mVideo1.configure(image = img1)
                self.mVideo1.image = img1

                imghsv = imutils.resize(imghsv, width = 300)
                # Display the resulting imghsv
                im2 = Image.fromarray(imghsv)
                img2 = ImageTk.PhotoImage(image = im2)

                self.mVideo2.config(bg = "gray50")
                self.mVideo2.configure(image = img2)
                self.mVideo2.image = img2

                mascaraV = imutils.resize(mascaraV, width = 300)
                # Display the resulting mascaraV
                im3 = Image.fromarray(mascaraV)
                img3 = ImageTk.PhotoImage(image = im3)

                self.mVideo3.config(bg = "gray50")
                self.mVideo3.configure(image = img3)
                self.mVideo3.image = img3

                mascaraM = imutils.resize(mascaraM, width = 300)
                # Display the resulting mascaraV
                im4 = Image.fromarray(mascaraM)
                img4 = ImageTk.PhotoImage(image = im4)

                self.mVideo4.config(bg = "gray50")
                self.mVideo4.configure(image = img4)
                self.mVideo4.image = img4
                self.mVideo4.after(10, self.visualizar)



    def foto(self):
        if self.cap is not None:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            # if frame is read correctly ret is True
            if ret == True:
                print(str(time.time()))
                # Our operations on the frame come here
                imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

                #Verde
                verdeBajo = np.array([self.vB.get(),
                                      self.sB.get(),
                                      self.bB.get()], np.uint8)
                verdeAlto = np.array([self.vA.get(),
                                      self.sA.get(),
                                      self.bA.get()], np.uint8)
                mascaraV = cv.inRange(imghsv, verdeBajo, verdeAlto)

                #Madura
                maduraBajo = np.array([self.mB.get(),
                                       self.sB.get(),
                                       self.bB.get()], np.uint8)
                maduraAlto = np.array([self.mA.get(),
                                       self.sA.get(),
                                       self.bA.get()], np.uint8)
                mascaraM = cv.inRange(imghsv, maduraBajo, maduraAlto)

                #Mascara tamaño
                tamBajo = np.array([self.mB.get(),
                                       self.sB.get(),
                                       self.bB.get()], np.uint8)
                tamAlto = np.array([self.vA.get(),
                                       self.sA.get(),
                                       self.bA.get()], np.uint8)
                mascaraT = cv.inRange(imghsv, tamBajo, tamAlto)

                contornosV, _ =cv.findContours(mascaraV, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                contornosM, _ =cv.findContours(mascaraM, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                contornosT, _ =cv.findContours(mascaraT, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                areaV = 0
                areaM = 0
                areaT = 0

                for c in contornosV:
                    areaV = cv.contourArea(c)

                for c in contornosM:
                    areaM = cv.contourArea(c)

                for c in contornosT:
                    areaT = cv.contourArea(c)

                #if self.areaMT > 8000 or self.areaVT > 8000:
                    #areaV = (self.areaVT + areaV) / 2
                    #areaM = (self.areaMT + areaM) / 2

                if (areaV > areaM):
                    print("V:" + str(areaV) + " M:" + str(areaM) + " T:" + str(areaT) + " |") 
                    areaV = areaV + areaM
                    print(str(areaV) + " |")

                    if (areaT > 10000 and areaT <= 36000): #Verde Chica
                        dato = "F"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Verde Chica Detectada")

                    if (areaT > 36000 and areaT <= 52000): #Verde Mediana
                        dato = "E"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Verde Mediana Detectada")

                    if (areaT > 52000 and areaT <= 80000): #Verde Grande
                        dato = "D"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Verde Grande Detectada")

                elif (areaM > areaV):
                    print("V:" + str(areaV) + " M:" + str(areaM) + " T:" + str(areaT) + " |") 
                    areaM = areaM + areaV
                    print(str(areaM) + " |")

                    if (areaT > 10000 and areaT <= 36000): #Madura Chica
                        dato = "C"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Madura Chica Detectada")

                    if (areaT > 36000 and areaT <= 52000): #Madura Mediana
                        dato = "B"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Madura Mediana Detectada")

                    if (areaT > 52000 and areaT <= 80000): #Madura Chica
                        dato = "A"
                        self.datos_pic.enviar_datos(dato)
                        print("Instruccion Madura Grande Detectada")

                areaV = 0
                areaM = 0
                areaT = 0
                print(str(time.time()))




    def widgets(self):
        frm = Frame(self.master, bg = "black", bd = 2)
        frm.grid(column = 0, row = 0, columnspan = 2, sticky = "nsew")
        frm1 = Frame(self.master, bg = "black")
        frm1.grid(column = 2, row = 0, sticky = "nsew") 
        frm2 = Frame(self.master, bg = "black")
        frm2.grid(column = 0, row = 1, columnspan = 3, sticky = "nsew")

        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.rowconfigure(0, weight = 5)
        self.master.rowconfigure(1, weight = 1)

        port = self.datos_pic.puertos
        baud = self.datos_pic.baudrates

        #frm
        self.mVideo1 = Label(frm, bg = "black")
        self.mVideo1.grid(column = 0, row = 0, padx = 1, pady = 1, sticky="nsew")

        self.mVideo2 = Label(frm, bg = "black")
        self.mVideo2.grid(column = 0, row = 1, padx = 1, pady = 1, sticky="nsew")

        self.mVideo3 = Label(frm, bg = "black")
        self.mVideo3.grid(column = 1, row = 0, padx = 1, pady = 1, sticky="nsew")

        self.mVideo4 = Label(frm, bg = "black")
        self.mVideo4.grid(column = 1, row = 1, padx = 1, pady = 1, sticky="nsew")
        
        #frm1
        Label(frm1, text = "Camara", bg = "black", fg = "white", font = ("Arial", 12, "bold")).pack(padx = 5, expand = 1)
        self.cb_cameras = ttk.Combobox(frm1, values = port, justify = "center", width = 12,
                                   font = ("Arial", 12, "bold"), state = "readonly")
        self.cb_cameras.pack(padx = 20, pady = 0, expand = 1)
        self.cb_cameras.config(values = "0 1 2 3")
        self.cb_cameras.current(0)

        Label(frm1, text = "Puertos COM", bg = "black", fg = "white", font = ("Arial", 12, "bold")).pack(padx = 5, expand = 1)
        self.cb_port = ttk.Combobox(frm1, values = port, justify = "center", width = 12,
                                   font = ("Arial", 12, "bold"), state = "readonly")
        self.cb_port.pack(padx = 20, pady = 0, expand = 1)
        if (len(port) > 0):
            self.cb_port.current(0)
        else:
            pass

        Label(frm1, text = "Baudrates", bg = "black", fg = "white", font = ("Arial", 12, "bold")).pack(padx = 5, expand = 1)
        self.cb_baud = ttk.Combobox(frm1, values = baud, justify = "center", width = 12,
                                   font = ("Arial", 12, "bold"), state = "readonly")
        self.cb_baud.pack(padx = 20, pady = 0, expand = 1)
        self.cb_baud.current(3)

        self.bt_conectar = Button(frm1, text = "Conectar", font = ("Arial", 12, "bold"), width = 12,
                                 bg = "green", fg = "white", command = self.iniciar)
        self.bt_conectar.pack(padx = 20, pady = 5, expand = 1)

        self.bt_buscar = Button(frm1, text = "Buscar", font = ("Arial", 12, "bold"), width = 12,
                               bg = "gray", fg = "white", command = self.actualizar)
        self.bt_buscar.pack(padx = 20, pady = 5, expand = 1)

        self.bt_desconectar = Button(frm1, text = "Desconectar", font = ("Arial", 12, "bold"), width = 12,
                                   bg = "red", fg = "white", command = self.pausar, state = "disable")
        self.bt_desconectar.pack(padx = 20, pady = 5, expand = 1)

        #frm2
        Label(frm2, text = "Color Madura Bajo", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 0, row = 0, padx = 20, pady = 4)
        self.mB = Scale(frm2, from_ = 0, to = 40, orient = HORIZONTAL, bg = "black", fg = "white")
        self.mB.grid(column = 0, row = 1, padx = 20, pady = 4)
        self.mB.set(10)
        self.mB.config(state = "disable")
        

        Label(frm2, text = "Color Madura Alto", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 0, row = 2, padx = 20, pady = 4)
        self.mA = Scale(frm2, from_ = 20, to = 60, orient = HORIZONTAL, bg = "black", fg = "white")
        self.mA.grid(column = 0, row = 3, padx = 20, pady = 4)
        self.mA.set(30)
        self.mA.config(state = "disable")


        Label(frm2, text = "Color Verde Bajo", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 1, row =     0, padx = 20, pady = 4, sticky="nsew")
        self.vB = Scale(frm2, from_ = 20, to = 60, orient = HORIZONTAL, bg = "black", fg = "white")
        self.vB.grid(column = 1, row = 1, padx = 20, pady = 4, sticky="nsew")
        self.vB.set(28)
        self.vB.config(state = "disable")
        

        Label(frm2, text = "Color Verde Alto", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 1, row = 2, padx = 20, pady = 4)
        self.vA = Scale(frm2, from_ = 40, to = 80, orient = HORIZONTAL, bg = "black", fg = "white")
        self.vA.grid(column = 1, row = 3, padx = 20, pady = 4)
        self.vA.set(60)
        self.vA.config(state = "disable")
        

        Label(frm2, text = "Saturacion Bajo", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 2, row = 0, padx = 20, pady = 4)
        self.sB = Scale(frm2, from_ = 0, to = 255, orient = HORIZONTAL, bg = "black", fg = "white")
        self.sB.grid(column = 2, row = 1, padx = 20, pady = 4)
        self.sB.set(60)
        self.sB.config(state = "disable")
        

        Label(frm2, text = "Saturacion Alto", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 2, row = 2, padx = 20, pady = 4)
        self.sA = Scale(frm2, from_ = 0, to = 255, orient = HORIZONTAL, bg = "black", fg = "white")
        self.sA.grid(column = 2, row = 3, padx = 20, pady = 4)
        self.sA.set(255)
        self.sA.config(state = "disable")
        

        Label(frm2, text = "Brillo Bajo", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 3, row = 0, padx = 20, pady = 4)
        self.bB = Scale(frm2, from_ = 0, to = 255, orient = HORIZONTAL, bg = "black", fg = "white")
        self.bB.grid(column = 3, row = 1, padx = 20, pady = 4)
        self.bB.set(0)
        self.bB.config(state = "disable")
        

        Label(frm2, text = "Brillo Alto", bg = "black", fg = "white",
             font = ("Arial", 8, "bold")).grid(column = 3, row = 2, padx = 20, pady = 4)
        self.bA = Scale(frm2, from_ = 0, to = 255, orient = HORIZONTAL, bg = "black", fg = "white")
        self.bA.grid(column = 3, row = 3, padx = 20, pady = 4)
        self.bA.set(255)
        self.bA.config(state = "disable")




    def actualizar(self):
        self.datos_pic.puertos_disponibles()
        port = self.datos_pic.puertos        
        self.cb_port.config(values = port)
        if (len(port) > 0):
            self.cb_port.current(0)
        else:
            pass




if __name__ == "__main__":
    root = Tk()
    root.config(bg = "gray30", bd = 4)
    root.title("CLASIFICADOR")
    root.config(bg = "black")

    #root.state('zoomed')
    #root.attributes('-zoomed', True)

    root.resizable(False, False) #Bloque la ventana y no permite expandirla
    root.geometry("1200x870") #Cambiamos las dimensiones de la ventana

    #  Obtenemos el largo y  ancho de la pantalla
    wtotal = root.winfo_screenwidth()
    htotal = root.winfo_screenheight()
    #  Guardamos el largo y alto de la ventana
    wventana = 1200
    hventana = 870

    #  Aplicamos la siguiente formula para calcular donde debería posicionarse
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2.2-hventana/2)

    #  Se lo aplicamos a la geometría de la ventana
    root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))

    app = Grafica(root)
    app.mainloop()