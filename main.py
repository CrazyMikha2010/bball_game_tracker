import cv2
from ultralytics import YOLO
import numpy as np
from menu_drawer.pygame_facade import PygameFacade
from court_scheme.court_drawer import courtDrawer
from court_scheme.keypoint_detector import keypointDetector
from object_detection.pl_bball_rim_detector import objectDetector
from court_scheme.homography import Homography
from object_detection.ball_cv import ballDetector
from score_counter.shotDetector import shotDetector


cap = cv2.VideoCapture("testing/videos/test1.mp4")
c = courtDrawer()
k = keypointDetector()
o = objectDetector()
b = ballDetector()
pg_facade = PygameFacade((1280, 720), "Mezh project")
score = 0
in3pts = False

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (1280, 720))

while True:
    pg_facade.clear_screen()
    ret, frame = cap.read()
    frame = o.detect(frame)
    b.detectBall(frame)
    src = k.getKeypointsNP(frame)
    dst = c.translated_detected_Keypoints
    h = Homography(src, dst)
    if o.playerCoords:
        player_pos = o.playerCoords[-1] # ((x1, y1), (x2, y2))
        player_pos = ((player_pos[0][0] + player_pos[1][0])//2, player_pos[1][1])
        coords = h.createHomography([player_pos])
        c.draw_points(coords, (0, 0, 255))
        in3pts = c.in3pts(coords[0])
        if in3pts:
            frame = pg_facade.putText(frame, (10, 500), "3pt", 5)
            print('3pt')
        else:
            frame = pg_facade.putText(frame, (10, 500), "2pt", 5)
            print('2pt')

    if len(b.path) >= 2:
        s = shotDetector(o.rimCoords[-1][0][0], o.rimCoords[-1][1][0], o.rimCoords[-1][0][1])
        if s.isIn(b.path[-2], b.path[-1]) and b.updated:
            score += 2 + 1 * in3pts
            b.updated = False

    frame = c.blit(frame, 10, 10, 270, 200, 0.7)
    frame = k.drawKeypoints(frame)
    frame = b.drawBall(frame)
    frame = pg_facade.putText(frame, (10, 600), f"score: {score}", 5)
    out.write(frame)
    # pg_facade.draw_image(0, 0, pg_facade.image_to_surface(frame))
    # pg_facade.update_screen()

cap.release()
out.release()
cv2.destroyAllWindows()

