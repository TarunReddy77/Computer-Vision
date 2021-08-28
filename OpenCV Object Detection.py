import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    img = cv2.resize(frame, (0,0), fx = 1.5, fy = 1.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = np.int0(cv2.goodFeaturesToTrack(gray, 500, 0.1, 3))
    # print(corners)
    for corner in corners:
        x, y = corner.ravel()
        img = cv2.circle(img, (x,y), 1, (0,0,255), -1)
        
    cv2.imshow('Image', img)

    if cv2.waitKey(0) == ord('x'):
        break
cv2.destroyAllWindows()