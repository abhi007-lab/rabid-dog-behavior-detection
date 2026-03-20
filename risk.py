def compute_risk(speed, direction):
    speed_score = min(speed / 15, 1)
    direction_score = min(direction / 1.2, 1)

    # weighted combination
    risk = 0.5 * speed_score + 0.5 * direction_score
    return risk