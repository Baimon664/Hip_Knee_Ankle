import numpy as np

def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    
    if abs(det) < 1.0e-6:
        return (None, np.inf)
    
    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return ((cx, cy), radius)

def getPoints(prediction_json):
    left = prediction_json[0]
    right = prediction_json[1]
    if(prediction_json[0]['x'] > prediction_json[1]['x']):
        left = prediction_json[1]
        right = prediction_json[0]
    return left['points'], right['points']

def get_three_points(points):
    points = points[:-1]
    p1 = points[(len(points) // 2) - 2]
    p2 = points[len(points) // 2]
    p3 = points[(len(points) // 2) + 2]
    return p1, p2, p3

def getCircle(femoral_circle_list):
    left_points, right_points = getPoints(femoral_circle_list)

    lp1, lp2, lp3 = get_three_points(left_points)
    rp1, rp2, rp3 = get_three_points(right_points)

    lp1 = [lp1['x'], lp1['y']]
    lp2 = [lp2['x'], lp2['y']]
    lp3 = [lp3['x'], lp3['y']]

    rp1 = [rp1['x'], rp1['y']]
    rp2 = [rp2['x'], rp2['y']]
    rp3 = [rp3['x'], rp3['y']]

    left_circle = define_circle(lp1, lp2, lp3)
    right_circle = define_circle(rp1, rp2, rp3)

    left_center, left_radius = left_circle
    right_center, right_radius = right_circle

    left_center = (int(left_center[1]), int(left_center[0]))
    right_center = (int(right_center[1]), int(right_center[0]))

    left_radius = int(left_radius)
    right_radius = int(right_radius)

    return left_center, left_circle, right_center, right_circle
