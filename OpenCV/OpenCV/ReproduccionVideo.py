import numpy as np
import cv2 as cv

cap = cv.VideoCapture('videoPrueba.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)

    cv.imshow('frame', gray)
    if cv.waitKey(25) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()