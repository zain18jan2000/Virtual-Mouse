import autopy
import cv2
import numpy as np
import handTrackingModule as htm

detector = htm.handDetector(maxHands=1)

cap = cv2.VideoCapture(0)
Wcam,Hcam = 700,580
cap.set(3,Wcam)
cap.set(4,Hcam)

Wscr, Hscr = autopy.screen.size()
print(Wscr,Hscr)
frameR =  100
plocx,plocy = 0,0
clocx,clocy = 0,0
smoothen = 5

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[9][1:]
        #print(x1, y1, x2, y2)

    # which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img,(frameR,frameR),(Wcam-2*frameR,Hcam-2*frameR),(255,0,255),5)
        if fingers[1] == 0 and fingers[2] == 1:

            x3 = np.interp(x1,(frameR,Wcam-2*frameR),(0,Wscr))
            y3 = np.interp(y1,(frameR,Hcam-2*frameR),(0,Hscr))

            # smoothening the cursor locaction values
            clocx = plocx + (x3-plocx) /smoothen
            clocy = plocy + (y3-plocy) /smoothen
            # move mouse pointer
            autopy.mouse.move(Wscr-clocx,clocy)

            # update cursor location
            plocx,plocy = clocx,clocy

            cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)

        if fingers[1] == 0 and fingers[2] == 0:
            length,img,lineinfo = detector.findDistance(8,12,img)
            print(length)
            if length < 40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(255,0,0))
                autopy.mouse.click()

    cv2.imshow("image",img)
    k = cv2.waitKey(5)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
