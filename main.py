import math
from random import randint

import cv2, cvzone, time, threading
from cvzone.HandTrackingModule import HandDetector
import mediapipe

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()
timer=''
def countdown(t=30):
    global timer
    while t!=-1:
        mins, secs=divmod(t,60)
        timer='{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t-=1

purple, white, black, green,red=(255,0,255), (255,255,255),(0,0,0), (0,255,0),(255,0,0)
c1, c2=purple, white
score=0
target=(150,350)
counter=0
restart,quit=False,False

detector = cvzone.HandTrackingModule.HandDetector(detectionCon=0.8)
while True:
    success, img=cap.read()
    img = cv2.flip(img, 1)
    if not success:
        print("Failed to grab frame")
        break
    if (cv2.waitKey(1) & 0xFF == ord('q')) or quit:
        print("Exiting...")
        break
    hands, img = detector.findHands(img, draw=False)
    if hands:
        lmList = hands[0]['lmList']
        x,y,w,h=hands[0]['bbox']
        x1, y1, _= lmList[5]
        x2, y2, _ = lmList[17]
        distance = math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2 )
        distanceCM = 6000/distance
        if timer=='':
            threading.Thread(target=countdown, args=(10,), daemon=True).start()
        if distanceCM<40:
            if x<target[0]<x+w and y<target[1]<y+h:
                c1, c2=(150,0,150), (200,200,200)
                counter+=1

        else:
            c1, c2=purple, white
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5,y-10))
        cv2.rectangle(img, (x-20,y-20),(x+w+20,y+h+20),purple,3)

    if counter:
        if counter==4:
            target=(randint(100,1100),randint(100,600))
            counter=0
            score+=1
    if timer:
        if timer=='00:00':
            if score>10:
                cvzone.putTextRect(img, f'Yay! You won!', (220,450), scale=4, colorT=black, colorR=white, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX )
            else:
                cvzone.putTextRect(img, f'Oof! You lost!', (220,450), scale=4, colorT=black, colorR=white, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX )
            cvzone.putTextRect(img, f'Restart', (400,550), scale=2, colorT=black, colorR=green, font=cv2.FONT_HERSHEY_DUPLEX)
            cvzone.putTextRect(img, f'Quit', (700,550), scale=2, colorT=black, colorR=red, font=cv2.FONT_HERSHEY_DUPLEX )

        else:
            cv2.circle(img, target, 30,c1, cv2.FILLED)
            cv2.circle(img, target, 20,c2, cv2.FILLED)
            cv2.circle(img, target, 10,c1, cv2.FILLED)

    cvzone.putTextRect(img, f'Press Q to quit', (500,50), scale=2, colorT=black, colorR=white)
    cvzone.putTextRect(img, f'Time : {timer}', (1030,50), scale=2, colorT=black, colorR=white)
    cvzone.putTextRect(img, f'Score : {score}', (1030,100), scale=2, colorT=black, colorR=white)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()