import cv2
import track_module.trackmodule as tm
import time
import math
import numpy as np
import pyautogui
import ctypes

# Get screen size
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print("Screen width: ", screen_width)
print("Screen height: ", screen_height)

cap = cv2.VideoCapture(0)

pTime = 0

detector = tm.HandDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    
    # Adjust the size of the frame
    img = cv2.flip(img, 1)  # Flip so that when hand moves right, cursor moves right too
    frame_height, frame_width, _ = img.shape
    scaleWidth = float(screen_width) / float(frame_width)
    scaleHeight = float(screen_height) / float(frame_height)

    if scaleHeight > scaleWidth:
        imgScale = scaleWidth
    else:
        imgScale = scaleHeight

    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    img = cv2.resize(img, (int(newX), int(newY)))   # Screen width: 1440, Screen height: 1080
    
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
        pyautogui.moveTo(x2+5, y2+30, 0.1)

        if x1 > x2:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)
            print("Clicking mouse")
            pyautogui.click()


    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Frame", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()