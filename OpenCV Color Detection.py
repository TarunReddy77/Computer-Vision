import cv2, numpy as np

cap = cv2.VideoCapture(0)
low_blue = np.array([0, 100, 150])
high_blue = np.array([20, 255, 255])

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Video', result)
    cv2.imshow('Mask', mask)
    if cv2.waitKey(10) == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()