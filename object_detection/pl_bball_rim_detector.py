from ultralytics import YOLO
import numpy as np
import cv2
import supervision as sv

class objectDetector:
    def __init__(self):
        self.model = YOLO("models/best.pt")
        # self.model = YOLO("models/nba.pt")
        self.ballCls = 0
        self.rimCls = 1
        self.playerCls = 2
        self.ballCoords = []
        self.rimCoords = []
        self.playerCoords = []

    def detect(self, im):
        results = self.model(im, conf=0.6)[0]
        self.rimPos = "undefined"
        for r in results:
            for box in r.boxes:
                clsID = int(box.cls)
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                if clsID == self.ballCls: # ball
                    center = (x1 + (x2-x1)//2, y1 + (y2-y1)//2)
                    r = (x2-x1)//2
                    # cv2.circle(im, center, r, (0, 0, 255), cv2.FILLED)
                    self.ballCoords.append((center, r))
                elif clsID == self.rimCls: # rim
                    cv2.line(im, (x1, y1), (x2, y1), (255, 255, 255), 2)
                    self.rimCoords.append( ((x1, y1), (x2, y2)) )
                else: # player
                    cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    self.playerCoords.append(((x1, y1), (x2, y2)))
        return self.drawBall(im)

    def drawBall(self, im):
        for center, radius in self.ballCoords[-10:]:
            continue
            cv2.circle(im, center, radius, (0, 0, 255), cv2.FILLED)
        return im

if __name__ == "__main__":
    d = objectDetector()
    cap = cv2.VideoCapture("/Users/mezhibovskiymikhail/Downloads/temp/video_2.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow("frame", d.detect(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
