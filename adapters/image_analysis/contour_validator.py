import cv2
import numpy as np
from exceptions.exception import DistanceValidationException
from utils.logger import get_logger

class ContourValidator:
    def is_rectangle(contour, angle_tolerance=10):
        # 1. Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * peri, True)

        # Rectangle must have exactly 4 points
        if len(approx) != 4:
            return False

        # 2. Optional: Check angles ≈ 90 degrees
        def angle(pt1, pt2, pt3):
            v1 = pt1 - pt2
            v2 = pt3 - pt2
            cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            return np.degrees(np.arccos(cosine))

        pts = approx.reshape(4, 2)
        angles = []

        for i in range(4):
            p1 = pts[i]
            p2 = pts[(i + 1) % 4]
            p3 = pts[(i + 2) % 4]
            angles.append(angle(p1, p2, p3))

        # all angles should be around 90°
        if all(abs(a - 90) < angle_tolerance for a in angles):
            return True

        return False


