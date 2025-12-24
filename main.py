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


court_drawer = courtDrawer()
keypoint_detector = keypointDetector()
object_detector = objectDetector()
ball_detector = ballDetector()
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
    pg_facade.clear_screen()
    ret, frame = cap.read()
    if not ret:
        break
    frame = object_detector.detect(frame, menu.settings[2], menu.settings[0])
    src = keypoint_detector.getKeypointsNP(frame)
    dst = court_drawer.translated_detected_Keypoints
    homography_matrix = Homography(src, dst)
    if object_detector.playerCoords:
        player_pos = object_detector.playerCoords[-1] # ((x1, y1), (x2, y2))
        ball_detector.detectBall(frame, object_detector.rimCoords[-1], player_pos)
        player_top = player_pos[0][1]
        player_pos = ((player_pos[0][0] + player_pos[1][0])//2, player_pos[1][1])
        coords = homography_matrix.createHomography([player_pos])
        if made:
            made_homo = homography_matrix.createHomography(made)
        if missed: missed_homo = homography_matrix.createHomography(missed)
        if homography_matrix.success:
            court_drawer.draw_points(coords, (0, 0, 255))
            in3pts = court_drawer.in3pts(coords[0])
        if ball_detector.path:
            ball_top = ball_detector.path[-1][1]
            if ball_top < player_top:
                if not flying:
                    shot_coords = player_pos
                flying = True
            else:
                flying = False


    if len(ball_detector.path) >= 2:
        if object_detector.rimCoords and ball_detector.updated:
            s = shotDetector(object_detector.rimCoords[-1][0][0], object_detector.rimCoords[-1][1][0], object_detector.rimCoords[-1][0][1])
            if ball_detector.path[-2][1] < object_detector.rimCoords[-1][0][1] < ball_detector.path[-1][1]:
                shot_coords = homography_matrix.createHomography([shot_coords])[0]
                if s.isIn(ball_detector.path[-2], ball_detector.path[-1]):
                    court_drawer.made.append(shot_coords)
                    if in3pts:
                        threePM += 1
                        threePA += 1
                        score += 3
                    else:
                        twoPM += 1
                        twoPA += 1
                        score += 2
                else:
                    court_drawer.missed.append(shot_coords)
                    if in3pts:
                        threePA += 1
                    else:
                        twoPA += 1
            ball_detector.updated = False

    stats[0] = twoPM + threePM
    stats[1] = twoPA + threePA
    stats[2] = int((stats[0] / max(stats[1], 1)) * 100)
    stats[3] = twoPM
    stats[4] = twoPA
    stats[5] = int((stats[3] / max(stats[4], 1)) * 100)
    stats[6] = threePM
    stats[7] = threePA
    stats[8] = int((stats[6] / max(stats[7], 1)) * 100)
    court_drawer.drawFGA()
    if menu.settings[4]: frame = court_drawer.blit(frame, 10, 10, 270, 200, 0.7)
    if menu.settings[3]: frame = keypoint_detector.drawKeypoints(frame)
    if menu.settings[1]: frame = ball_detector.drawBall(frame)
    pg_facade.draw_image(0, 0, pg_facade.image_to_surface(frame))
    stats_drawer.draw_score(score)
    stats_drawer.draw_stats(stats)
    stats_drawer.draw_in3pts(in3pts)
    stats_drawer.draw_flying(flying)
    pg_facade.update_screen()
    surface_array = pg.surfarray.array3d(pg_facade.screen)
    frame = cv2.cvtColor(surface_array.swapaxes(0, 1), cv2.COLOR_RGB2BGR)
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
