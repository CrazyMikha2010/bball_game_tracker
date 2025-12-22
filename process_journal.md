Goals:

- [x] Распознавать мяч
- [x] Распознавать кольцо
- [x] Распознавать забитый
- [x] Различать двух от трех очкового

27.11

tried pose estimation with mediapipe for the first time. 
problem is that it doesn't track mutiple people, so I'm gonna use YOLO in future 

28.11

set goals

29.11 - 1.12

trained yolov8 nano model on two different datasets

5.12 

learned how to count scored goal

1.12 - 6.12 

trained yolov8n model to detect player, basketball, and rim, and also pose detection model to detect court keypoints

8.12 

https://www.youtube.com/watch?v=3JczIfnC1N4

significant limitations with camera angles and quality - models are trained on specific datasets -> 

landmark detection works only on courts filmed in NBA format

ball should be seen clearly

9.12 

had to reconsider my view on things - started annotating my own dataset

made video

10.12

filmed video

11.12

annotated one frame from each second (236 frames) for object detection and pose estimation (skeletons)

12.12 - 13.12 

trained models

12.12 - 17.12

DANO break

18.12

now I'm able to draw court in top left corner, geometrically.

found the formula for all it's dimensions

19.12 

completed homography - with opencv perspective transfrom

20.12 

now I'm able to tell if a person is in 3pt line or nah

21.12

added pygame functionality

