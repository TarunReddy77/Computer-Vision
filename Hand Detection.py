import cv2, numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon = 0.5)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 920)
cx, cy, w, h = 100, 100, 200, 200
color = (128, 54, 42)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    img = detector.findHands(frame)
    lmList, _ = detector.findPosition(frame)
    frame = cv2.rectangle(frame, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), color, -1)
    if lmList:
        dist, *_ = detector.findDistance(8, 12, img)
        print(dist)
        if dist < 70:
            x, y = lmList[8]
            if cx-w//2 < x < cx+w//2 and cy-h//2 < y < cy+h//2:
                color = (255, 50, 150)
                cx, cy = x, y
            else:
                color = (128, 54, 42)
            
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()