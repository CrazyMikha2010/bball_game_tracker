from ultralytics import YOLO
import cv2
import supervision as sv
import numpy as np

class keypointDetector:
    def __init__(self):
        self.VerteLabelAnnotator = sv.VertexLabelAnnotator(
            color=sv.Color.GREEN,
            text_color=sv.Color.BLACK,
            border_radius=5
        )
        self.courtDetector = YOLO("models/best2.pt")
        # self.courtDetector = YOLO("models/pose.pt")

    def getKeypointsSV(self, im):
        result = self.courtDetector(im)[0]
        keypoints = sv.KeyPoints.from_ultralytics(result)
        return keypoints

    def getKeypointsNP(self, im):
        result = self.courtDetector(im)[0]
        keypoints = result.keypoints.data.cpu().numpy()
        if keypoints.shape[0] == 0:
            return np.array([], dtype=np.float32).reshape(0, 2)
        keypointsXY = keypoints[0, :, :2]
        return keypointsXY.astype(np.float32)

    def drawKeypoints(self, im):
        annotated_frame = self.VerteLabelAnnotator.annotate(
            scene=im.copy(),
            key_points=self.getKeypointsSV(im)
        )
        return annotated_frame



if __name__ == "__main__":
    k = keypointDetector()
    cap = cv2.VideoCapture("/Users/mezhibovskiymikhail/Downloads/temp/video_2.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(1)