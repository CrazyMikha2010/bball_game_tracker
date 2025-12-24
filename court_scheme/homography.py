import cv2
import numpy as np

class Homography:
    def __init__(self, src, dst):
        self.success = False
        if src.shape[0] >= 4:
            self.H, status = cv2.findHomography(src, dst)
            self.success = True

    def createHomography(self, coords):
        if self.success:
            coords_arr = np.array(coords).reshape(-1, 1, 2).astype(np.float32)
            coords_transformed = cv2.perspectiveTransform(coords_arr, self.H)
            coords_transformed = coords_transformed.reshape(-1, 2).tolist()
            return coords_transformed
        return []

