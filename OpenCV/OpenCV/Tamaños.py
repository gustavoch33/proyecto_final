import cv2 as cv
import numpy as np
from DetectorObjetos import *

#Cargamos el detector del marcador aruco
parametros = cv.aruco.DetectorParameters_create()
diccionario = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_100)

#Cargamos el detector de objetos
detector = DetectorFonfoHomogeneo()

#Parametros del HSV
def nada(x):
    pass

cv.namedWindow('Parametros')
cv.createTrackbar('HMin', 'Parametros', 0, 180, nada)
cv.createTrackbar('HMax', 'Parametros', 70, 180, nada) #Parametro H
cv.createTrackbar('SMin', 'Parametros', 100, 255, nada)
cv.createTrackbar('SMax', 'Parametros', 255, 255, nada) #Parametro S
cv.createTrackbar('VMin', 'Parametros', 0, 255, nada)
cv.createTrackbar('VMax', 'Parametros', 255, 255, nada) #Parametro V

#Realizamos la videocaptura
cap = cv.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

while True:
    #Realizamos la lectura de la camara
    ret, frame = cap.read()
    if ret == False: break

    #Detectamos el marcador aruco
    esquinas, _, _ = cv.aruco.detectMarkers(frame, diccionario, parameters = parametros)
    esquinasEnt = np.int0(esquinas)
    cv.polylines(frame, esquinasEnt, True, (0,0,255), 5)

    #Perimetro del aruco
    perimetroAruco = 1
    try: 
        perimetroAruco = cv.arcLength(esquinasEnt[0], True)
    except:
        pass
    #print(perimetroAruco)

    #Proporcion en cm
    proporcionCm = perimetroAruco / 16
    #print(proporcioCm)

    #Obtenemos los valores del HSV
    Hmin = cv.getTrackbarPos('HMin', 'Parametros')
    Hmax = cv.getTrackbarPos('HMax', 'Parametros')
    Smin = cv.getTrackbarPos('SMin', 'Parametros')
    Smax = cv.getTrackbarPos('SMax', 'Parametros')
    Vmin = cv.getTrackbarPos('VMin', 'Parametros')
    Vmax = cv.getTrackbarPos('VMax', 'Parametros')

    #Detectamos los objetos
    contornos, area = detector.deteccionObjetos(frame, Hmin, Hmax, Smin, Smax, Vmin, Vmax)

    for cont in contornos:
        if (area > 3500):
            print(area)

            #Dibujamos el contorno del objeto
            cv.polylines(frame, [cont], True, (0,255,0), 2)

            #A partir de poligono anterior vamos a obtener un rectangulo
            rectangulo = cv.minAreaRect(cont)
            (x,y), (an, al), angulo = rectangulo

            #Pasamos el ancho y el alto de pixeles a cm
            ancho = an / proporcionCm
            alto = al / proporcionCm

            #Dibujamos un circulo en la mitad del rectangulo
            #cv.circle(frame, (int(x), int(y)), 5, (255,255,0), -1)

            #Vamos a dibujar el rectangulo que ya obtuvimos
            rect = cv.boxPoints(rectangulo) #Obtenemos el rectangulo
            rect = np.int0(rect)            #Aseguramos que toda la info este en enteros

            #Dibujamos el rectangulo
            cv.polylines(frame, [rect], True, (0,255,0), 2)
            #Mostramos la info en pixeles
            cv.putText(frame, "Ancho: {} cm".format(round(ancho, 1)), (int(x), int(y-15)), cv.LINE_AA, 0.8, (150,0,255), 2)
            cv.putText(frame, "Largo: {} cm".format(round(alto, 1)), (int(x), int(y+15)), cv.LINE_AA, 0.8, (75,0,75), 2)

    #Mostramos los fotogramas
    cv.imshow("Medicion de objetos", frame)

    #Si presionamos ESC
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
