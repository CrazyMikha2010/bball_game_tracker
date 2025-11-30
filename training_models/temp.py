from ultralytics import YOLO

model = YOLO("../runs_nano/detect/train5/weights/best.pt")
results = model.train(data="Basketball.v1i.yolov8/data.yaml", epochs=25, batch=24)
