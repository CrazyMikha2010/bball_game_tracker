import cv2
from ultralytics import YOLO
import numpy as np
import pygame as pg
from menu_drawer.pygame_facade import PygameFacade
from court_scheme.court_drawer import courtDrawer
from court_scheme.keypoint_detector import keypointDetector
from object_detection.pl_bball_rim_detector import objectDetector
from court_scheme.homography import Homography
from object_detection.ball_cv import ballDetector
from score_counter.shotDetector import shotDetector
from menu_drawer.stats_drawer import statsDrawer
from menu_drawer.menu import Menu



c = courtDrawer()
k = keypointDetector()
o = objectDetector()
b = ballDetector()
pg_facade = PygameFacade((1280, 720), "Mezh project")
menu = Menu((1280, 720), pg_facade)
stats_drawer = statsDrawer(pg_facade)
score = 0
in3pts = False
flying = False
shot_coords = (-1, -1)

twoPA, threePA, twoPM, threePM = 0, 0, 0, 0
made, missed = [], []
made_homo, missed_homo = made, missed

stats = [0] * 9

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cap = cv2.VideoCapture("testing/videos/test3.MOV")
out = cv2.VideoWriter('output_video.mp4', fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (1280, 720))
while True:
    while not menu.is_start:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            menu.update(event)
        menu.draw()
    print(menu.settings)
    pg_facade.clear_screen()
    ret, frame = cap.read()
    if not ret:
        break
    frame = o.detect(frame)
    b.detectBall(frame)
    src = k.getKeypointsNP(frame)
    dst = c.translated_detected_Keypoints
    h = Homography(src, dst)
    if o.playerCoords:
        player_pos = o.playerCoords[-1] # ((x1, y1), (x2, y2))
        player_top = player_pos[0][1]
        player_pos = ((player_pos[0][0] + player_pos[1][0])//2, player_pos[1][1])
        coords = h.createHomography([player_pos])
        if made:
            made_homo = h.createHomography(made)
        if missed: missed_homo = h.createHomography(missed)
        if h.success:
            c.draw_points(coords, (0, 0, 255))
            in3pts = c.in3pts(coords[0])
        if b.path:
            ball_top = b.path[-1][1]
            if ball_top < player_top:
                if not flying:
                    shot_coords = player_pos
                flying = True
            else:
                flying = False


    if len(b.path) >= 2:
        if o.rimCoords and b.updated:
            s = shotDetector(o.rimCoords[-1][0][0], o.rimCoords[-1][1][0], o.rimCoords[-1][0][1])
            if b.path[-2][1] < o.rimCoords[-1][0][1] < b.path[-1][1]:
                shot_coords = h.createHomography([shot_coords])[0]
                if s.isIn(b.path[-2], b.path[-1]) and b.updated:
                    c.made.append(shot_coords)
                    if in3pts:
                        threePM += 1
                        threePA += 1
                    else:
                        twoPM += 1
                        twoPA += 1
                else:
                    c.missed.append(shot_coords)
                    if in3pts:
                        threePA += 1
                    else:
                        twoPA += 1
            b.updated = False

    stats[0] = twoPM + threePM
    stats[1] = twoPA + threePA
    stats[2] = int((stats[0] / max(stats[1], 1)) * 100)
    stats[3] = twoPM
    stats[4] = twoPA
    stats[5] = int((stats[3] / max(stats[4], 1)) * 100)
    stats[6] = threePM
    stats[7] = threePA
    stats[8] = int((stats[6] / max(stats[7], 1)) * 100)
    c.drawFGA()
    frame = c.blit(frame, 10, 10, 270, 200, 0.7)
    frame = k.drawKeypoints(frame)
    frame = b.drawBall(frame)
    # out.write(frame)
    pg_facade.draw_image(0, 0, pg_facade.image_to_surface(frame))
    stats_drawer.draw_score(score)
    stats_drawer.draw_stats(stats)
    stats_drawer.draw_in3pts(in3pts)
    stats_drawer.draw_flying(flying)
    pg_facade.update_screen()

cap.release()
out.release()
cv2.destroyAllWindows()

