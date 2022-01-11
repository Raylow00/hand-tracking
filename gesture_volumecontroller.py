import cv2
import trackmodule as tm
import time
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = tm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()

minVol = volumeRange[0]
maxVol = volumeRange[1]
vol = volPer = 0
volBar = 350

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

        # Hand range 25-250
        # Volume range -65-0
        vol = np.interp(length, [25, 250], [minVol, maxVol])
        volBar = np.interp(length, [25, 250], [350, 150])
        volPer = np.interp(length, [25, 250], [0, 100])
        print(int(volPer))

        volume.SetMasterVolumeLevel(vol, None)

        if length < 30:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

    
    cv2.rectangle(img, (50, 150), (75, 350), (0, 255, 0), 2)
    cv2.rectangle(img, (50, int(volBar)), (75, 350), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (44, 390), cv2.FONT_HERSHEY_COMPLEX, 0.6, (200, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)