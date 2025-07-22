import cv2 as cv
import numpy as np

class DetectorFonfoHomogeneo():
    def __init__(self):
        pass

    def deteccionObjetos(self, frame, Hmin, Hmax, Smin, Smax, Vmin, Vmax):
        area = 0

        #Convertir imagen a escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #Crea una mascara con umbral adaptativo
        mask = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 19, 5)

        maskB = np.array([Hmin,Smin,Vmin], np.uint8)
        maskA = np.array([Hmax,Smax,Vmax], np.uint8)
        maskX = cv.inRange(imghsv, maskB, maskA)

        #Encuentra contornos
        contornos, _ = cv.findContours(maskX, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #Creamos una lista donde almacenamos los objetos
        objetosContornos = []

        #Si encontramos contornos entramos al for
        for cnt in contornos:
            #Medimos en area de los contornos
            area = cv.contourArea(cnt)
            #Si el area es mayor a 2000 agregamos el objeto a la lista
            if area > 3500:
                objetosContornos.append(cnt)

        cv.imshow("MASK", imghsv)

        return objetosContornos, area
