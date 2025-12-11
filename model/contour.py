import random

# List of human-readable color names and their RGB values
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255)
}

def get_random_human_color():
    name = random.choice(list(COLORS.keys()))
    rgb = COLORS[name]
    return name, rgb

# Example usage
color_name, color_rgb = get_random_human_color()
print(f"Random color: {color_name}, RGB: {color_rgb}")

class Contour:
    """
    Solidarity : is there a hole in the contour (area / convex area)
    Extent : how well the contour “fills” the bounding rectangle.
    """
    def __init__(self,contour, area, perimeter, bounding_box, aspect_ratio, extent, solidity):
        self.uid = id(self)
        # Assign random color for visualization in overlays
        self.color = get_random_human_color()
        self.contour = contour
        self.area = area
        self.perimeter = perimeter
        self.bounding_box = bounding_box
        self.aspect_ratio = aspect_ratio
        self.extent = extent
        self.solidity = solidity
        self.score = 0.0
        self.circularity = (4 * 3.1416 * area) / (perimeter * perimeter) if perimeter != 0 else 0.0

    def set_contour(self, contour):
        self.contour = contour

    def get_contour(self):
        return self.contour

    def __lt__(self, other):
        return self.score < other.score


    def __repr__(self):
        return (
            f"Contour(id={self.uid}, color={self.color}, area={self.area}, "
            f"perimeter={self.perimeter}, bounding_box={self.bounding_box}, "
            f"aspect_ratio={self.aspect_ratio:.2f}, extent={self.extent:.2f}, "
            f"solidity={self.solidity:.2f}, circularity={self.circularity:.2f}, score={self.score:.2f})"
        )
        return (f"Contour(id={self.uid} color={self.color} area={self.area}, perimeter={self.perimeter}, "
                f"bounding_box={self.bounding_box}, aspect_ratio={self.aspect_ratio:.2f}, "
                f"extent={self.extent:.2f}, solidity={self.solidity:.2f}) Score={self.score:.2f}")