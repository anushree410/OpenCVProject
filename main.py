import math

import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

detecter = HandDetector(detectionCon=0.8)
while True:
    success, img=cap.read()
    hands, img = detecter.findHands(img)
    if hands:
        lmList = hands[0]['lmList']
        print(lmList[5])
        x1, y1, _= lmList[5]
        x2, y2, _ = lmList[17]
        print(math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2 ))
    cv2.imshow("Image",img)
    cv2.waitKey(1)