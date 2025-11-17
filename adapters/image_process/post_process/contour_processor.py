import cv2
import numpy as np

class ContourProcessor:
    @staticmethod
    def get_contour_info(countour) -> dict:
        """
        Calculate area and perimeter of a contour.\n
        Properties Explained:
        Area : Number of pixels inside the contour.\n
        Perimeter : Length of the contour boundary.\n
        Bounding Box : Smallest rectangle that can enclose the contour.\n
        Aspect Ratio : Width to height ratio of the bounding box.\n
        Extent : How much of the bounding box is filled (compactness).\n
        Solidity: How concave or convex the object is (1.0 = perfectly convex).\n
        Returns a dictionary with these properties.
        
        """
        # Basic properties

        # Area : number of pixels inside the contour
        area = cv2.contourArea(countour)

        # Perimeter : length of the contour boundary
        perimeter = cv2.arcLength(countour, True)

        # Bounding Box : smallest rectangle that can enclose the contour
        x, y, w, h = cv2.boundingRect(countour)

        # Aspect Ratio : width to height ratio of the bounding box
        aspect_ratio = float(w) / h
        
        # Extent : how much of the bounding box is filled (compactness).
        rect_area = w * h
        extent = area / rect_area  # fraction of bounding box filled by the contour

        # Hull / Solidity: how concave or convex the object is (1.0 = perfectly convex).
        hull = cv2.convexHull(countour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area

        return {"area": area, "perimeter": perimeter, "bounding_box": (x, y, w, h), "aspect_ratio": aspect_ratio, "extent": extent, "solidity": solidity}