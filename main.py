import math
import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

detecter = HandDetector(detectionCon=0.8)
while True:
    success, img=cap.read()
    if not success:
        print("Failed to grab frame")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break
    hands, img = detecter.findHands(img)
    if hands:
        lmList = hands[0]['lmList']
        # print(lmList[5])
        x1, y1, _= lmList[5]
        x2, y2, _ = lmList[17]
        distance = math.sqrt((x1-x2) ** 2 + (y1-y2) ** 2 )
        distanceCM = 6000/distance
        print("DISTANCE in CM: ",distanceCM, distance)
    cv2.imshow("Image",img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()