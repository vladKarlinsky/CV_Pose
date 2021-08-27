import cv2
import mediapipe
import time
import PoseModule as pm
import numpy as np

cap = cv2.VideoCapture(0)
dec = pm.poseDetector()
count_curls = 0
dir = 0
dir_str = 'GO DOWN'

while True:
    dec.clearLmlist()
    success, img = cap.read()
    img = dec.findPos(img, False)
    lmList = dec.findPosition(img, True)
    if len(lmList) != 0:

        # Right arm
        angle = dec.findAngle(img, 12, 14, 16)
        # Left arm
        # angle = dec.findAngle(img, 11, 13, 15) - feel free to comment out this line when needed

        # Choosing angles that are required to preform a bicep curl correctly
        meta_data_curl_up = 40
        meta_data_curl_down = 145
        per = np.interp(angle, (meta_data_curl_up, meta_data_curl_down), (0, 100))

        # check if curl is preformed correctly
        if per == 100:  # curl is at right position
            if dir == 0:  # checking if direction is down
                count_curls += 0.5
                dir = 1  # change direction
                dir_str = 'GO UP'
        if per == 0:
            if dir == 1:
                count_curls += 0.5
                dir = 0  # change direction
                dir_str = 'GO DOWN'

        print(img.shape)
        cv2.rectangle(img, (0, 0), (250, 150), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, f'#{int(count_curls)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
        cv2.putText(img, 'BICEP CURLS', (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        cv2.putText(img, f'{dir_str}', (30, 140), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
    cv2.imshow("Trainer project", img)

    cv2.waitKey(1)
