import cv2
import numpy as np
import supervision as sv
from math import hypot

class courtDrawer:
    def __init__(self):
        self.H, self.W = 680, 1280
        self.court = np.ones((self.H, self.W, 3), np.uint8)*255
        self.actualW, self.actualH = 28.65, 15.24
        self.actualKeypoints = np.array([
            (0, 0),
            (0, 0.91),
            (0, 5.18),
            (0, 10.06),
            (0, 14.33),
            (0, self.actualH),
            (self.actualW/2, self.actualH),
            (self.actualW / 2, 0),
            (5.79, 5.18),
            (5.79, 10.06),
            (self.actualW, self.actualH),
            (self.actualW, self.actualH - 0.91),
            (self.actualW, self.actualH - 5.18),
            (self.actualW, self.actualH - 10.06),
            (self.actualW, self.actualH - 14.33),
            (self.actualW, 0),
            (self.actualW - 5.79, self.actualH - 10.06),
            (self.actualW-5.79, self.actualH - 5.18)
        ])
        self.detectedKeypoints = np.array([
            (self.actualW, 0),
            (self.actualW, self.actualH - 14.33),
            (self.actualW, self.actualH - 10.06),
            (self.actualW, self.actualH - 5.18),
            (self.actualW, self.actualH - 0.91),
            (self.actualW, self.actualH),
            (self.actualW - 5.79, self.actualH - 10.06),
            (self.actualW - 5.79, self.actualH - 5.18)
        ])
        self.translated_detected_Keypoints = (self.detectedKeypoints * [self.W / self.actualW, self.H / self.actualH]).astype(int)
        self.translatedKeypoints = (self.actualKeypoints * [self.W / self.actualW, self.H / self.actualH]).astype(int)
        self.VerteLabelAnnotator = sv.VertexLabelAnnotator(
            color=sv.Color.GREEN,
            text_color=sv.Color.BLACK,
            border_radius=5
        )
        self.made, self.missed = [], []
        self.drawCourt()

    def _update(self):
        self.court = np.ones((self.H, self.W, 3), np.uint8) * 255
        self.drawCourt()

    def _translate(self, x, y):
        return (self._translateX(x), self._translateY(y))

    def _translateX(self, x):
        return int(x/self.actualW*self.W)

    def _translateY(self, y):
        return int(y/self.actualH*self.H)

    def drawKeypoints(self):
        tmp = np.array([self.translated_detected_Keypoints])
        self.court = self.VerteLabelAnnotator.annotate(
            scene=self.court.copy(),
            key_points=sv.KeyPoints(xy=tmp)
        )

    def drawCourt(self):
        # half court
        cv2.line(self.court, self.translatedKeypoints[6], self.translatedKeypoints[7], (0, 0, 0), 2)
        # circle in the middle and on free throw lines
        for x in [5.79, self.actualW/2, self.actualW-5.79]:
            cv2.circle(self.court, (self._translateX(x), self.H//2), self._translateX(1.83), (0, 0, 0), 2)
        # 3pt line
        cv2.ellipse(self.court, self._translate(1.58, self.actualH / 2), (self._translateY(7.24), self._translateY(7.24)), 0, -69, 69, (0, 0, 0), 2)
        cv2.ellipse(self.court, self._translate(self.actualW-1.58, self.actualH / 2), (self._translateY(7.24), self._translateY(7.24)), 0, 111, 249, (0, 0, 0), 2)
        for idx in [1,4]:
            cv2.line(self.court, self.translatedKeypoints[idx], (self._translateX(4.27), self.translatedKeypoints[idx,1]), (0, 0, 0), 2)
            cv2.line(self.court, self.translatedKeypoints[idx+10],(self._translateX(self.actualW-4.27), self.translatedKeypoints[idx+10,1]), (0, 0, 0), 2)
        # paint rect
        for idxs in [[2,9], [12,16]]:
            cv2.rectangle(self.court, self.translatedKeypoints[idxs[0]], self.translatedKeypoints[idxs[1]], (0, 0, 0), 2)
        # basket
        for x in [1.55, self.actualW-1.55]:
            cv2.circle(self.court, (self._translateX(x), self.H//2), 10, (0, 0, 0), 2)
            if x == 1.55:
                cv2.ellipse(self.court, (self._translateX(x), self.H // 2), (55, 55), 0, -90, 90, (0, 0, 0), 2)
                cv2.line(self.court, self._translate(1.22, 6.7), self._translate(1.22, self.actualH-6.7), (0, 0, 0), 2)
            else:
                cv2.ellipse(self.court, (self._translateX(x), self.H // 2), (55, 55), 0, 90, 270, (0, 0, 0), 2)
                cv2.line(self.court, self._translate(self.actualW-1.22, 6.7), self._translate(self.actualW-1.22, self.actualH - 6.7), (0, 0, 0), 2)

    def draw_points(self, coords, color):
        self._update()
        for coord in coords:
            cv2.circle(self.court, (int(coord[0]), int(coord[1])), 5, color, 2)

    def in3pts(self, coord):
        x, y = coord
        if x >= self._translateX(self.actualW - 4.27):
            if self.translatedKeypoints[1][1] <= y <= self.translatedKeypoints[4][1]:
                return False
        else:
            rim_x, rim_y = self._translate(self.actualW - 1.58, self.actualH / 2)
            r = self._translateY(6.2)
            dist = hypot(x - rim_x, y - rim_y)
            if dist <= r:
                return False

        return True

    def check(self):
        from random import randint
        for _ in range(100):
            x, y = randint(0, self.W), randint(0, self.H)
            if x >= self._translateX(self.actualW - 4.27):
                if self.translatedKeypoints[1][1] <= y <= self.translatedKeypoints[4][1]:
                    cv2.circle(self.court, (x, y), 5, (0, 255, 0), 2)
            else:
                rim_x, rim_y = self._translate(self.actualW - 1.58, self.actualH / 2)
                r = self._translateY(7.24)
                dist = hypot(x-rim_x, y-rim_y)
                if dist <= r:
                    cv2.circle(self.court, (x, y), 5, (0, 255, 0), 2)

    def blit(self, im, x, y, w, h, alpha):
        blitim = self.court[:, self.W//2:self.W]
        blitim = np.rot90(blitim)
        blitim = cv2.resize(blitim, (w, h))
        reg = im[y:y+h, x:x+w]
        im[y:y+h, x:x+w] = cv2.addWeighted(blitim, alpha, reg, 1 - alpha, 0)
        return im

    def show(self):
        cv2.imshow('court drawer', self.court)
        cv2.waitKey(0)

    def drawFGA(self):
        for miss in self.missed:
            cv2.drawMarker(self.court, (int(miss[0]), int(miss[1])), (0, 0, 255),markerType=cv2.MARKER_CROSS,markerSize=15,thickness=2)
        for make in self.made:
            cv2.drawMarker(self.court, (int(make[0]), int(make[1])), (255, 255, 0),markerType=cv2.MARKER_STAR,markerSize=15,thickness=2)



if __name__ == "__main__":
    c = courtDrawer()
    c.drawKeypoints()
    c.check()
    c.show()

