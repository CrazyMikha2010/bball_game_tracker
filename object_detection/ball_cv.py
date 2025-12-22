import cv2
import numpy as np

lower = np.array([2, 120, 20])
upper = np.array([7, 200, 255])


class ballDetector():
    def __init__(self):
        self.path = []
        self.updated = True

    def detectBall(self, frame):
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV, lower, upper)
        frame_masked = cv2.bitwise_and(frame, frame, mask=mask)
        contours, hierarchy = cv2.findContours(cv2.cvtColor(frame_masked, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if area > 35 and abs(1 - (w/h)) < 0.2 :
                self.path.append((int(x+w/2), int(y+h/2)))
                self.updated = True

    def drawBall(self, frame):
        for coord in self.path:
            cv2.circle(frame, coord, 5, (255, 0, 0), 2)
        return frame
