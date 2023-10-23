import cv2
import numpy as np
import time
import datetime


cap = cv2.VideoCapture('video.mp4')

min_width_react =50
min_height_react = 40


count_line_position1 = 550
count_line_position2 = 350

algo= cv2.bgsegm.createBackgroundSubtractorMOG()

class Car:
    def __init__(self, number, x ,y):
        self.number = number
        self.x = x
        self.y = y
    def speed(self, elapsed_time, number):
        elapsed_time = elapsed_time
        print(elapsed_time)
        if elapsed_time == 0:
            elapsed_time = 1
        else: elapsed_time = elapsed_time
        v = 50 / elapsed_time
        v = v * 3.6
        # v = v / 120
        v = int(v)
        print(f"Vechicle number: {number}, speed: {v}")


def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy = y+y1
    return cx,cy

detect = []
offset = 6
counter1 = 0
countrt2 = 0


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
    elapsed_time = 0


    cv2.line(frame,(25,count_line_position1),(1200,count_line_position1),(255,127,0),3)
    cv2.line(frame,(25,count_line_position2),(1200,count_line_position2),(255,127,0),3)
    

    for(i,c) in enumerate(counterSahpe):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w>=min_width_react) and (h>=min_height_react)
        if not validate_counter:
            continue
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.putText(frame, 'Vehicle: ' + str(counter1), (x,y-20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,244,0), 2) 
        center = center_handle(x,y,w,h)
        detect.append(center)
        detect.append
        start_time = time.time()

        cv2.circle(frame,center,4,(0,0,255),-1)

        for (x,y) in detect:
            if y<(count_line_position1 + offset) and y>(count_line_position1 - offset):
                counter1+=1
                cv2.line(frame,(25,count_line_position1),(1200,count_line_position1),(255,127,0),5)
                car = counter1
                car = Car(counter1, x, y)
                detect.remove((x,y))
                end_time = time.time()
                elapsed_time = end_time - start_time
                elapsed_time += 3
                car.speed(elapsed_time, counter1)
                #print("Vehicle Counter: " + str(counter1))

       
    
    cv2.putText(frame,"Vehicle Counter: " + str(counter1),(375,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)


     #cv2.imshow('detecter' , dilatada)

    cv2.imshow('Video Original', frame)

    key =  cv2.waitKey(27)
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release() 