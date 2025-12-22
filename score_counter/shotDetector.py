import cv2
import numpy as np


class shotDetector:
    def __init__(self, rimX1, rimX2, rimY):
        self.rimY = rimY
        self.rimX1 = rimX1
        self.rimX2 = rimX2

    def isIn(self, prev, next):
        # y = ax + b
        if prev[0] - next[0] != 0:
            a = (prev[1]-next[1])/(prev[0]-next[0])
        else:
            a = (prev[1] - next[1])
        b = prev[1] - a * prev[0]
        # x = (y - b) / a
        if a != 0:
            cross_x = (self.rimY - b) / a
        else:
            cross_x = self.rimY - b
        return self.rimX1-5 <= cross_x <= self.rimX2+5 and prev[1] <= self.rimY <= next[1]


