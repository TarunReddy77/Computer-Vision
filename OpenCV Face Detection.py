import cv2, numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for face in faces:
        x, y, w, h = face.ravel()
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 4)
        roi = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi, 1.3, 5)
        for eye in eyes:
            ex, ey, ew, eh = eye.ravel()
            cv2.rectangle(frame, (x+ex,y+ey), (x+ex+ew, y+ey+eh), (255,0,0), 4)
            # break
    cv2.imshow('Face', frame)
    #print(faces)
    if cv2.waitKey(1) == ord('x'):
        break
cv2.destroyAllWindows()