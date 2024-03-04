import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success , img = cap.read()
    img = cv2.resize(img , (1280 , 720))
    #img = cv2.imread("AiTrainer/test.png")
    img = detector.findPose(img , False)
    lmList = detector.findPosition(img , draw=False)
    if len(lmList) !=0:
        #print(lmList)
        # Right arm
        angle = detector.findAngle(img , 12 , 14 , 16)

        # Left arm
        #detector.findAngle(img , 11 , 13 , 15)
        per = np.interp(angle , (200 , 30) , (0 , 100))
        print(per)

        #Check for dumble curls
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0

        cv2.putText(img , f'{int(count)}' , (50 , 100) , cv2.FONT_HERSHEY_PLAIN , 15 , (255 , 0 , 0) , 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 300), cv2.FONT_HERSHEY_PLAIN, 5 , (255, 0, 0), 5)

    cv2.imshow("Image" , img)
    cv2.waitKey(1)