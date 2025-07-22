#Importamos librerias
import numpy as np
import cv2 as cv
from time import sleep

#Vamos a capturar el objeto que queremos identificar
cap = cv.VideoCapture(1) #Selecionamos la camara con la que se trabajara
while(True):
    ret, frame = cap.read() #Leemos el video
    cv.imshow('Objeto', frame) #Mostramos el video en pantalla
    if cv.waitKey(1) == 27: #Si presionamos ESC cerramos el video
        break

cv.imwrite('objeto.jpg', frame) #Guardamos la ultima captura del video como imagen
cap.release() #Cerramos
cv.destroyAllWindows()

#Leemos la imagen del objeto que queremos identificar
obj = cv.imread('objeto.jpg', 0) #Leemos la imagen
recorte = obj[160:300, 230:380] #Recortamos la imagen para que solo quede el objeto [fila:fila, colum:colum]
cv.imshow('objeto', recorte) #Mostramos en pantalla el objeto a reconocer
sleep(2)

#Una vez tenemos el objeto definido tomamos la foto con el resto de objetos
cap = cv.VideoCapture(1) #Selecionamos la camara con la que se trabajara
while(True):
    ret2, frame2 = cap.read() #Leemos el video
    cv.imshow('Deteccion', frame2) #Mostramos el video en pantalla
    if cv.waitKey(1) == 27: #Si presionamos ESC cerramos el video
        break

cv.imwrite('Deteccion.jpg', frame2) #Guardamos la ultima captura del video como imagen
cap.release() #Cerramos
cv.destroyAllWindows()

#Mostramos la imagen con todos los objetos
img = cv.imread('Deteccion.jpg', 3)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #Pasamos la imagen a escala de grises
cv.imshow('Deteccion', img)

#Empezamos el algoritmo
w, h = recorte.shape[::-1] #Extraemos el ancho y el alto del recorte del objeto
deteccion = cv.matchTemplate(gray, recorte, cv.TM_CCOEFF_NORMED) #Realizamos la deteccion por patrones
umbral = 0.75 #Asignamos un umbral para filtrar objetos parecidos
ubi = np.where(deteccion >= umbral) #La ubicacion de los objetos la guardamos cuando 
for pt in zip (*ubi[::-1]): #Creamos un for para dibujar los rectangulos
    cv.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0,255,0), 1)

cv.imshow('Deteccion', img)

cv.waitKey(0)