import numpy as np
import cv2 as cv

def nada(x):
    pass

cv.namedWindow('Parametros')
cv.createTrackbar('TMin', 'Parametros', 0, 179, nada)
cv.createTrackbar('TMax', 'Parametros', 0, 179, nada) #Parametro H
cv.createTrackbar('PMin', 'Parametros', 0, 255, nada)
cv.createTrackbar('PMax', 'Parametros', 0, 255, nada) #Parametro S
cv.createTrackbar('LMin', 'Parametros', 0, 255, nada)
cv.createTrackbar('LMax', 'Parametros', 0, 255, nada) #Parametro V
cv.createTrackbar('Kernel X', 'Parametros', 1, 30, nada)
cv.createTrackbar('Kernel Y', 'Parametros', 1, 30, nada) #Filtro

#Crear el video
cap = cv.VideoCapture(2)
while(1):
    ret, frame = cap.read()
    if ret:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        Tmin = cv.getTrackbarPos('TMin', 'Parametros')
        Tmax = cv.getTrackbarPos('TMax', 'Parametros')
        Pmin = cv.getTrackbarPos('PMin', 'Parametros')
        Pmax = cv.getTrackbarPos('PMax', 'Parametros')
        Lmin = cv.getTrackbarPos('LMin', 'Parametros')
        Lmax = cv.getTrackbarPos('LMax', 'Parametros')

        colorOscuro = np.array([Tmin, Pmin, Lmin])
        colorBrilla = np.array([Tmax, Pmax, Lmax])
        #print(colorOscuro)
        #print(colorBrilla)

        mascara = cv.inRange(hsv, colorOscuro, colorBrilla)

        kernelx = cv.getTrackbarPos('Kernel X', 'Parametros')
        kernely = cv.getTrackbarPos('Kernel Y', 'Parametros')

        kernel = np.ones((kernelx, kernely), np.uint8)
        #print(kernel)
        mascara = cv.morphologyEx(mascara, cv.MORPH_CLOSE, kernel)
        mascara = cv.morphologyEx(mascara, cv.MORPH_OPEN, kernel)

        contornos, _ = cv.findContours(mascara, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame, contornos, -1, (0,0,0), 2)

        cv.imshow('Camara', frame)
        cv.imshow('Mascara', mascara)

        if cv.waitKey(1) == 27:
            cv.detroyAllWindows()

cap.release()
