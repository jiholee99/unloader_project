class Contour:
    """
    Solidarity : is there a hole in the contour (area / convex area)
    Extent : how well the contour “fills” the bounding rectangle.
    """
    def __init__(self,contour, area, perimeter, bounding_box, aspect_ratio, extent, solidity):
        self.contour = contour
        self.area = area
        self.perimeter = perimeter
        self.bounding_box = bounding_box
        self.aspect_ratio = aspect_ratio
        self.extent = extent
        self.solidity = solidity
        self.score = 0.0

    def set_contour(self, contour):
        self.contour = contour

    def get_contour(self):
        return self.contour

    def __repr__(self):
        return (f"Contour(area={self.area}, perimeter={self.perimeter}, "
                f"bounding_box={self.bounding_box}, aspect_ratio={self.aspect_ratio:.2f}, "
                f"extent={self.extent:.2f}, solidity={self.solidity:.2f}) Score={self.score:.2f}")