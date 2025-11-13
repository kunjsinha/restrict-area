import cv2
import numpy as np

points = []
polygon_finalized = False 

def click_event(event, x, y, flags, param):
    global polygon_finalized
    if event == cv2.EVENT_LBUTTONDOWN and not polygon_finalized:
        points.append((x, y))  
    if event == cv2.EVENT_RBUTTONDOWN: 
        points.clear() #reset
        polygon_finalized = False

video_path = "input.mp4"
cap = cv2.VideoCapture(video_path)

cv2.namedWindow("Video")
cv2.setMouseCallback("Video", click_event)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    for p in points:
        cv2.circle(frame, p, 5, (0, 0, 255), -1)

    if len(points) > 1:
        for i in range(len(points) - 1):
            cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 2)

    if polygon_finalized and len(points) > 2:
        cv2.polylines(frame, [np.array(points, np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)

    cv2.imshow("Video", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):  #quit
        break
    elif key == ord('p') and len(points) > 2:  #close shape
        polygon_finalized = True

cap.release()
cv2.destroyAllWindows()
