import cv2 as cv

cap = cv.VideoCapture(2, cv.CAP_DSHOW)

guayabaV = cv.CascadeClassifier("guayabaVerde.xml")

def nada(x):
    pass

cv.namedWindow('Parametros')
cv.createTrackbar('ScaleFactorD', 'Parametros', 5, 10, nada)
cv.createTrackbar('ScaleFactorU', 'Parametros', 0, 10, nada)
cv.createTrackbar('Neighbors', 'Parametros', 170, 200, nada)
cv.createTrackbar('Size1', 'Parametros', 70, 200, nada)
cv.createTrackbar('Size2', 'Parametros', 78, 200, nada)

scale = 6
neigh = 50

while True:
    ret, frame = cap.read()
    #print(ret)
    if ret == True:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        scaleS = float(str(cv.getTrackbarPos('ScaleFactorD', 'Parametros'))+"."+
                      str(cv.getTrackbarPos('ScaleFactorU', 'Parametros')))
        scale = float(scaleS)
        neigh = int(cv.getTrackbarPos('Neighbors', 'Parametros'))
        s1 = int(cv.getTrackbarPos('Size1', 'Parametros'))
        s2 = int(cv.getTrackbarPos('Size2', 'Parametros'))

        #print(scale, type(scale))
        #print(neigh, type(neigh))

        fruit = guayabaV.detectMultiScale(gray,
                                          scaleFactor = scale,
                                          minNeighbors = neigh,
                                          minSize = (s1,s2))

        for (x, y, w, h) in fruit:
            cv.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 2)
            cv.putText(frame, "Guayaba", (x,y-10), 2, 0.7, (255,0,0), 2, cv.LINE_AA)

        cv.imshow("frame", frame)

        if cv.waitKey(1) == 27:
            break

cap.release()
cv.destroyAllWindows()
