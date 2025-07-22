import numpy as np
import cv2 as cv
from time import sleep, time
import threading


cap = cv.VideoCapture(1, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

ret = cap.set(cv.CAP_PROP_FRAME_WIDTH, 350) #Cambiamos el largo del video en pixeles
#ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT, 400) #Cambiamos lo alto del video en pixeles

#print(cap.get(cv.CAP_PROP_FRAME_WIDTH)) #Obtenemos la resolucio del video a lo largo en pixeles
#print(cap.get(cv.CAP_PROP_FRAME_HEIGHT)) #Obtenemos la resolucio del video a lo alto en pixeles

tiempo = 0
countdown = None

def hilo():
    global tiempo
    global countdown

    for i in range(8):
        tiempo = tiempo - 1
        sleep(1)
        print(tiempo)

        if tiempo == 5:
            foto()
        
        if tiempo == 4:
            print("Retirar")

    print("Tiempo finalizado\n")

def visualizar():
    global tiempo
    global countdown

    _, frame2 = cap.read()
    # Our operations on the frame come here
    imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #Verde
    verdeBajo = np.array([31,70,0], np.uint8)
    verdeAlto = np.array([60,255,255], np.uint8)
    mascaraV = cv.inRange(imghsv, verdeBajo, verdeAlto)

    #Madura
    maduraBajo = np.array([10,70,0], np.uint8)
    maduraAlto = np.array([30,255,255], np.uint8)
    mascaraM = cv.inRange(imghsv, maduraBajo, maduraAlto)

    contornosV, v =cv.findContours(mascaraV, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contornosM, m =cv.findContours(mascaraM, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if(v is not None and m is not None):
        for c in contornosV:
            areaV = cv.contourArea(c)
            if (areaV > 3500):
                #print("Verde Detectada")
                #print(time())
                detect = True
                x, y, w, h = cv.boundingRect(c)
                cv.rectangle(frame2, (x,y), (x+w,y+h), (255,0,0), 2)
                cv.putText(frame2, "Area: " + str(areaV), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                cv.putText(frame2, "Guayaba Verde", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                if tiempo == 0:
                    print("Hilo Iniciado")
                    tiempo = 8
                    countdown = threading.Thread(target = hilo)
                    countdown.start()


        for c in contornosM:
            areaM = cv.contourArea(c)
            if (areaM > 3500):
                #print("Madura Detectada")
                #print(time())
                detect = True
                x, y, w, h = cv.boundingRect(c)
                cv.rectangle(frame2, (x,y), (x+w,y+h), (255,255,0), 2)
                cv.putText(frame2, "Area: " + str(areaM), (x,y-5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                cv.putText(frame2, "Guayaba Madura", (x,y-25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
                if tiempo == 0:
                    print("Hilo Iniciado")
                    tiempo = 8
                    countdown = threading.Thread(target = hilo)
                    countdown.start()

    else:
        #print("No detecto")
        pass

    

    # Display the resulting frame
    #cv.imshow("Video HSV", imghsv)
    #cv.imshow("Video binarizado Verde", mascaraV)
    #cv.imshow("Video binarizado Amarillo", mascaraM)
    cv.imshow("Imagen Detectada", frame2);


def foto():
    global cap
    #if cv.waitKey(1) == ord('t'):
    # Our operations on the frame come here
    _, frame3 = cap.read()
    imghsv = cv.cvtColor(frame3, cv.COLOR_BGR2HSV)

    #Verde
    verdeBajo = np.array([31,70,0], np.uint8)
    verdeAlto = np.array([60,255,255], np.uint8)
    mascaraV = cv.inRange(imghsv, verdeBajo, verdeAlto)

    #Madura
    maduraBajo = np.array([10,70,0], np.uint8)
    maduraAlto = np.array([30,255,255], np.uint8)
    mascaraM = cv.inRange(imghsv, maduraBajo, maduraAlto)

    contornosV, _ =cv.findContours(mascaraV, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contornosV:
        areaV = cv.contourArea(c)
        if (areaV > 3500):
            print("Instruccion Verde")

    contornosM, _ =cv.findContours(mascaraM, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contornosM:
        areaM = cv.contourArea(c)
        if (areaM > 3500):
            print("Instruccion Madura")



while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #foto()
    visualizar()
    #print("Corriendo")
    #cv.imshow("Video de entrada", frame)

    if cv.waitKey(1) == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
