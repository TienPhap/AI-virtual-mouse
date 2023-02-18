import cv2
import numpy as np
import time
import pyautogui
import HandTracking as ht
import autopy   # Install using "pip install autopy"
import sys
import streamlit as St
### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size
kt=1
thumb_old=0
a = St.selectbox(
        'Bạn muốn chon ngon nao de dieu khien chuot',
        ( 'ngon cai' ,'ngon tro' ,  'ngon giua', 'ngon ap ut' , 'ngon ut' ))
b = St.selectbox(
        'Bạn muốn chon ngon nao de dieu khien scroll',
        ( 'ngon cai' ,'ngon tro' ,  'ngon giua', 'ngon ap ut' , 'ngon ut' ))

c= St.selectbox(
        'Bạn muốn chon ngon nao de click1',
        ( 'ngon cai' ,'ngon tro' ,  'ngon giua', 'ngon ap ut' , 'ngon ut' ))
d = St.selectbox(
        'Bạn muốn chon ngon nao de click2',
        ( 'ngon cai' ,'ngon tro' ,  'ngon giua', 'ngon ap ut' , 'ngon ut' ))

e = St.selectbox(
        'Bạn muốn chon ngon nao de giu chuot',
        ( 'ngon cai' ,'ngon tro' ,  'ngon giua', 'ngon ap ut' , 'ngon ut' ))
batdau = St.button("bat dau")
def suyketqua(a):
    if a == "ngon cai":
        return fingers[0]==1
    elif a == "ngon tro":
        return fingers[1]==1
    elif a == "ngon giua":
        return fingers[2]==1
    elif a == "ngon ap ut":
        return fingers[3]==1
    elif a == "ngon ut":
        return  fingers[4]==1
if batdau:
    while True:
        success, img = cap.read()
        img = detector.findHands(img)                       # Finding the hand
        lmlist, bbox = detector.findPosition(img)           # Getting position of hand
        print(lmlist)
        if len(lmlist)!=0:
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            fingers = detector.fingersUp()
     # Checking if fingers are upwards
            print(fingers)
            cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box

            if suyketqua(a):     # If fore finger is up and middle finger is down
                x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
                y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))
                curr_x = \
                        prev_x + (x3 - prev_x)/smoothening
                curr_y = prev_y + (y3 - prev_y) / smoothening
                autopy.mouse.move(screen_width - curr_x, curr_y)    # Moving the cursor
                cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                prev_x, prev_y = curr_x, curr_y
            # thả chuột trái và click
            if suyketqua(c) and suyketqua(d) and kt!= suyketqua(d):
                pyautogui.mouseUp(button='left')
                pyautogui.click()
            kt=suyketqua(d)
            # giữ chuột trái
            if suyketqua(e):
                pyautogui.mouseDown(button='left')
            # scroll up
            if suyketqua(b):
                if thumb_old==0:
                    thumb_old=lmlist[4][2]
                else:
                    pyautogui.scroll(lmlist[4][2]-thumb_old)
            # Thoát
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                sys.exit(0)

                ''' length, img, lineInfo = detector.findDistance(8, 12, img)
    
                if length < 40:     # If both fingers are really close to each other
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.mouseDown(button='left')
                else:
                   pyautogui.mouseUp(button='left')
                    #autopy.mouse.click()   # Perform Click Left Mouse
                    #pyautogui.click(button='right') # Click Right Mouse'''




        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)