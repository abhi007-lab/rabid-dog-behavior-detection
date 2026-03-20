import math

history = {}

def update_behavior(obj_id, pos):
    if obj_id not in history:
        history[obj_id] = []

    history[obj_id].append(pos)

    if len(history[obj_id]) > 10:
        history[obj_id].pop(0)

def calculate_speed(obj_id):
    pts = history.get(obj_id, [])
    if len(pts) < 2:
        return 0

    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    return math.hypot(x2-x1, y2-y1)

def direction_change(obj_id):
    pts = history.get(obj_id, [])
    if len(pts) < 3:
        return 0

    (x1,y1),(x2,y2),(x3,y3) = pts[-3], pts[-2], pts[-1]

    v1 = (x2-x1, y2-y1)
    v2 = (x3-x2, y3-y2)

    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.hypot(*v1)
    mag2 = math.hypot(*v2)

    if mag1 * mag2 == 0:
        return 0

    angle = math.acos(dot/(mag1*mag2))
    return abs(angle)