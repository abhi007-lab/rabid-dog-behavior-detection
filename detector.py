from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_dogs(frame):
    results = model(frame)[0]
    boxes = []

    for box in results.boxes:
        cls = int(box.cls[0])
        if cls == 16:  # dog class
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            boxes.append((x1, y1, x2, y2))

    return boxes