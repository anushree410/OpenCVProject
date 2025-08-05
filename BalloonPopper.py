from PIL import Image
import numpy as np
import cvzone, time, cv2, threading, math
from balloons import BalloonGifs
from cvzone.HandTrackingModule import HandDetector
from random import randint
# import GameState
gif=BalloonGifs()
gif_frames=gif.getRandomBalloon()

# game=GameState()
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

def draw_balloon(frame, gif_frames, idx, target):
    gif_frame = gif_frames[idx]
    gif_np = np.array(gif_frame)
    gif_bgr = cv2.cvtColor(gif_np[..., :3], cv2.COLOR_RGB2BGR)
    alpha = gif_np[..., 3] / 255.0

    x_offset, y_offset = target
    y1, y2 = y_offset, y_offset + gif_bgr.shape[0]
    x1, x2 = x_offset, x_offset + gif_bgr.shape[1]

    if y2 <= frame.shape[0] and x2 <= frame.shape[1]:
        roi = frame[y1:y2, x1:x2]
        for c in range(3):
            roi[..., c] = (alpha * gif_bgr[..., c] + (1 - alpha) * roi[..., c]).astype(np.uint8)
        frame[y1:y2, x1:x2] = roi

purple, white, black, green,red=(255,0,255), (255,255,255),(0,0,0), (0,255,0),(255,0,0)
c1, c2=purple, white
score=0
target=(150,350)
counter=0
frame_idx = 0
num_gif_frames = len(gif_frames)
detector = cvzone.HandTrackingModule.HandDetector(detectionCon=0.8)
counter=0
restart,quit=False,False

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    height, width = frame.shape[:2]
    hands, img = detector.findHands(frame, draw=False)

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
                counter+=1
        else:
            c1, c2=purple, white
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5,y-10))
        cv2.rectangle(img, (x-20,y-20),(x+w+20,y+h+20),purple,3)
        if timer=='00:00':
            if distanceCM<40 and x<700<x+w and y<550<y+h:
                quit=True
            if distanceCM<40 and x<400<x+w and y<550<y+h:
                score=0
                threading.Thread(target=countdown, args=(10,), daemon=True).start()
    if counter:
        if counter==4:
            target=(randint(100,1100),randint(100,600))
            counter=0
            gif_frames=gif.getRandomBalloon()
            frame_idx=0
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
            draw_balloon(frame, gif_frames, frame_idx, target)
    cvzone.putTextRect(img, f'Press Q to quit', (500,50), scale=2, colorT=black, colorR=white)
    cvzone.putTextRect(img, f'Time : {timer}', (1030,50), scale=2, colorT=black, colorR=white)
    cvzone.putTextRect(img, f'Score : {score}', (1030,100), scale=2, colorT=black, colorR=white)

    cv2.imshow("Webcam with GIF", frame)

    frame_idx = (frame_idx + 1) % num_gif_frames

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
