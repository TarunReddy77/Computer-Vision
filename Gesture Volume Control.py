import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7) # Detection Confidence of 0.7 seemed to work best.

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False) # Returns a list of co-ordinates of key points on hands.
    if len(lmList) != 0:
        tx, ty = lmList[4][1], lmList[4][2] # lmList[4] refers to co-ordinates of tip of thumb.
        ix, iy = lmList[8][1], lmList[8][2] # lmList[8] refers to co-ordinates of tip of index finger.
        cx, cy = (tx + ix) // 2, (ty + iy) // 2 # (cx, cy) refers to the center point of the line between tips of thumb and index finger. 

        cv2.circle(img, (tx,ty), 8, (255,0,0,), -1)
        cv2.circle(img, (ix,iy), 8, (255,0,0,), -1)
        cv2.circle(img, (cx,cy), 8, (255,0,0,), -1)
        cv2.line(img, (tx,ty), (ix,iy), (0,255,255), 3)

        length = math.hypot(tx-ix, ty-iy)

        if length < 50:
            cv2.circle(img, (cx,cy), 8, (255,255,0,), -1)

        vol = np.interp(length, [50, 150], [minVol, maxVol]) # To convert the vol range from distance on screen to format suitable to change volume.
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (30,180), (50,350), (0,255,0), 1)
    vol_bar = int(np.interp(volume.GetMasterVolumeLevel(), [-65,0], [350,180]))
    cv2.rectangle(img, (30,vol_bar), (50,350), (0,255,0), -1) # To display the volume level on screen.
    # vol_per = int(np.interp(vol_bar, [350,180], [0,100]))
    # cv2.putText(img, f'{int(vol_per)} %', (20, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) # To calculate the frame rate.

    cv2.imshow("Img", img)
    if cv2.waitKey(1) == ord('x'):
        break
