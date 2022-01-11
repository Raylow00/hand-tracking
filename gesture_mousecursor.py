import cv2
import trackmodule as tm
import time
import math
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)

pTime = 0

detector = tm.HandDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print("Length: ", length)

        # Move mouse
        print("Moving mouse cursor")
        pyautogui.moveTo(cx, cy, 0.01)

        if length < 30:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

            # Click cursor
            print("Click")
            pyautogui.click()


    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)