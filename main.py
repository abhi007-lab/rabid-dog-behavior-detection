import cv2
from detector import detect_dogs
from behavior import update_behavior, calculate_speed, direction_change
from risk import compute_risk

def process_frame(frame, tracker):
    detections = detect_dogs(frame)
    objects = tracker.update(detections)

    alerts = []

    for obj_id, (cx, cy) in objects.items():
        update_behavior(obj_id, (cx, cy))

        speed = calculate_speed(obj_id)
        direction = direction_change(obj_id)

        avg_risk = compute_risk(speed, direction)

        # -------- LABEL LOGIC --------
        if avg_risk < 0.3:
            label = "NORMAL"
            color = (0,255,0)

        elif avg_risk < 0.7:
            label = "AGGRESSIVE"
            color = (0,165,255)

        else:
            label = "SUSPECTED RABID"
            color = (0,0,255)

            # store alert
            alerts.append({
                "id": obj_id,
                "risk": avg_risk,
                "cx": cx,
                "cy": cy
            })

        # draw text
        cv2.putText(frame,
                    f"{label} ({avg_risk:.2f})",
                    (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2)

    return frame, alerts