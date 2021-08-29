import cv2, numpy as np
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 900)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prev_time = 0; cur_time = 0
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, c = img.shape

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(landmarks.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == 8:
                    cv2.circle(img, (cx,cy), 15, (255, 255, 0), -1)
            mpDraw.draw_landmarks(img, landmarks, mpHands.HAND_CONNECTIONS)

    cur_time = time.time()
    fps = int(1/(cur_time - prev_time))
    prev_time = cur_time
    cv2.putText(img, str(fps), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,200), 4, cv2.LINE_AA)

    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()