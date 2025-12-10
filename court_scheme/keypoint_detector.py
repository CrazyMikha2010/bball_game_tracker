from ultralytics import YOLO
import cv2
import supervision as sv
from court_scheme.court_drawer import courtDrawer

class keypointDetector:
    def __init__(self):
        self.VerteLabelAnnotator = sv.VertexLabelAnnotator(
            color=sv.Color.GREEN,
            text_color=sv.Color.BLACK,
            border_radius=5
        )
        self.courtDetector = YOLO("models/pose.pt")
        self.dst = courtDrawer().translatedKeypoints

    def getKeypoints(self, im):
        result = self.courtDetector(im)[0]
        keypoints = sv.KeyPoints.from_ultralytics(result)
        return keypoints

    def drawKeypoints(self, im):
        annotated_frame = self.VerteLabelAnnotator.annotate(
            scene=im.copy(),
            key_points=self.getKeypoints(im)
        )
        return annotated_frame

    def createHomography(self, im):
        src = self.getKeypoints(im).xy
        H, status = cv2.findHomography(src, self.dst)


if __name__ == "__main__":
    k = keypointDetector()
    c = courtDrawer()
    cap = cv2.VideoCapture("/Users/mezhibovskiymikhail/Downloads/temp/video_2.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(1)