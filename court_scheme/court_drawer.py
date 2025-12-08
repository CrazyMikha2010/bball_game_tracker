import cv2
import numpy as np

class courtDrawer:
    def __init__(self):
        self.H, self.W = 680, 1280
        self.court = np.ones((self.H, self.W, 3), np.uint8)*255
        self.actualW, self.actualH = 28.65, 15.24
        self.actualKeypoints = [
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
        ]
        self.translatedKeypoints = [self._translate(x, y) for x, y in self.actualKeypoints]
        self.drawCourt()

    def _translate(self, x, y):
        return (int(x/self.actualW*self.W), int(y/self.actualH*self.H))

    def drawKeypoints(self):
        for idx, keypoint in enumerate(self.translatedKeypoints):
            cv2.circle(self.court, keypoint, 5, (255, 0, 0), cv2.FILLED)
            # cv2.putText(self.court, str(idx), keypoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    def drawCourt(self):
        # half court
        cv2.line(self.court, self.translatedKeypoints[6], self.translatedKeypoints[7], (0, 0, 0), 2)
        # circle in the middle and on free throw lines
        for x in [5.79, self.actualW/2, self.actualW-5.79]:
            cv2.circle(self.court, (int(x/self.actualW*self.W), self.H//2), int(1.83/self.actualW*self.W), (0, 0, 0), 2)
        # 3pt line
        cv2.ellipse(self.court, self._translate(1.58, self.actualH / 2), (int(7.24 / self.actualH * self.H), int(7.24 / self.actualH * self.H)), 0, -69, 69, (0, 0, 0), 2)
        cv2.ellipse(self.court, self._translate(self.actualW-1.58, self.actualH / 2), (int(7.24 / self.actualH * self.H), int(7.24 / self.actualH * self.H)), 0, 111, 249, (0, 0, 0), 2)
        for idx in [1,4]:
            cv2.line(self.court, self.translatedKeypoints[idx], (int(4.27/self.actualW*self.W), self.translatedKeypoints[idx][1]), (0, 0, 0), 2)
            cv2.line(self.court, self.translatedKeypoints[idx+10],(int(self.W-4.27 / self.actualW * self.W), self.translatedKeypoints[idx+10][1]), (0, 0, 0), 2)
        # paint rect
        for idxs in [[2,9], [12,16]]:
            cv2.rectangle(self.court, self.translatedKeypoints[idxs[0]], self.translatedKeypoints[idxs[1]], (0, 0, 0), 2)
        # basket
        for x in [1.55, self.actualW-1.55]:
            cv2.circle(self.court, (int(x/self.actualW*self.W), self.H//2), 10, (0, 0, 0), 2)
            if x == 1.55:
                cv2.ellipse(self.court, (int(x / self.actualW * self.W), self.H // 2), (55, 55), 0, -90, 90, (0, 0, 0), 2)
                cv2.line(self.court, self._translate(1.22, 6.7), self._translate(1.22, self.actualH-6.7), (0, 0, 0), 2)
            else:
                cv2.ellipse(self.court, (int(x / self.actualW * self.W), self.H // 2), (55, 55), 0, 90, 270, (0, 0, 0), 2)
                cv2.line(self.court, self._translate(self.actualW-1.22, 6.7), self._translate(self.actualW-1.22, self.actualH - 6.7), (0, 0, 0), 2)
        self.drawKeypoints()

    def blit(self, im, x, y, w, h, alpha):
        blitim = cv2.resize(self.court, (w, h))
        reg = im[y:y+h, x:x+w]
        im[y:y+h, x:x+w] = cv2.addWeighted(blitim, alpha, reg, 1 - alpha, 0)
        return im


if __name__ == "__main__":
    c = courtDrawer()
    c.drawCourt()
