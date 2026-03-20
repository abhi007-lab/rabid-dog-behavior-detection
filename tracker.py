import math

class Tracker:
    def __init__(self):
        self.objects = {}
        self.id_count = 0

    def update(self, detections):
        new_objects = {}

        for box in detections:
            x1, y1, x2, y2 = box
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2

            matched_id = None

            for obj_id, (px, py) in self.objects.items():
                dist = math.hypot(cx - px, cy - py)
                if dist < 50:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.id_count
                self.id_count += 1

            new_objects[matched_id] = (cx, cy)

        self.objects = new_objects
        return self.objects