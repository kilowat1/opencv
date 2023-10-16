import cv2
import numpy as np


cap = cv2.VideoCapture('video.mp4')

min_width_react = 80
min_height_react = 80

count_line_position = 550

algo= cv2.bgsegm.createBackgroundSubtractorMOG()
while True:
    ret,frame = cap.read()
    grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey , (3,3),5)
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE , (5,5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE , kernel)
    counterSahpe,h = cv2.findContours(dilatada, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    

    for(i,c) in enumerate(counterSahpe):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (w>=min_height_react)
        if not validate_counter:
            continue

        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)



    cv2.imshow('detecter' , dilatada)

    cv2.imshow('Video Original', frame)

    key =  cv2.waitKey(1)
    if key == 1:
        break

cv2.destroyAllWindows()
cap.release()
