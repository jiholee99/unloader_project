import cv2
import numpy as np

from exceptions.exception import ImagePostProcessingException

class ImagePostProcessor:
    @staticmethod
    def detect_contours(mask_image, min_area = 50000):
        """Detect contours in the binary mask image."""
        try:
            mask = cv2.bitwise_not(mask_image)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
            return valid_contours
        except Exception as e:
            raise ImagePostProcessingException(f"Error detecting contours",e)

    @staticmethod
    def fill_holes_in_mask(mask):
        """
        Fill holes inside black objects (white background)
        by detecting and filling inner contours.
        """
        # Ensure binary
        mask = (mask > 0).astype(np.uint8) * 255

        # Invert because we want the object to be white for contour detection
        inv = cv2.bitwise_not(mask)

        # Find contours and hierarchy
        contours, hierarchy = cv2.findContours(inv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        if hierarchy is None:
            return mask

        # Draw and fill only the internal (child) contours
        for i in range(len(contours)):
            # hierarchy[i][3] == -1 → no parent (external)
            # hierarchy[i][3] != -1 → has parent (hole)
            if hierarchy[0][i][3] != -1:
                cv2.drawContours(inv, contours, i, 255, -1)  # Fill hole

        # Invert back to black object, white background
        filled = cv2.bitwise_not(inv)

        return filled
    
    @staticmethod
    def is_contour_square(contour, epsilon=0.01, side_ratio_tol=0.15, angle_tol=15):
        """
        Check if a contour is approximately square-shaped.
        Stricter: requires 4 corners, nearly equal side lengths, and ~90° angles.

        Args:
            contour: The contour to check.
            epsilon: Polygon approximation accuracy (lower = stricter shape fit).
            side_ratio_tol: Allowed relative difference between side lengths (0.1 = 10%).
            angle_tol: Allowed deviation from 90° for angles (degrees).

        Returns:
            bool: True if the contour is approximately a square, False otherwise.
        """
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon * peri, True)

        if len(approx) != 4:
            return False

        # Calculate side lengths
        pts = approx.reshape(-1, 2)
        sides = [np.linalg.norm(pts[i] - pts[(i + 1) % 4]) for i in range(4)]

        # Check if opposite sides are roughly equal
        ratio1 = abs(sides[0] - sides[2]) / max(sides[0], sides[2])
        ratio2 = abs(sides[1] - sides[3]) / max(sides[1], sides[3])
        if ratio1 > side_ratio_tol or ratio2 > side_ratio_tol:
            return False

        # Check if adjacent sides are roughly equal (square not rectangle)
        mean_side = np.mean(sides)
        if np.max(np.abs(np.array(sides) - mean_side)) / mean_side > side_ratio_tol:
            return False

        # Check for right angles
        def angle_between(v1, v2):
            cosang = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            return np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))

        angles = []
        for i in range(4):
            v1 = pts[(i + 1) % 4] - pts[i]
            v2 = pts[(i - 1) % 4] - pts[i]
            angles.append(angle_between(v1, v2))

        if not all(abs(a - 90) < angle_tol for a in angles):
            return False

        return True