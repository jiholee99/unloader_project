import cv2
import numpy as np

def show_scaled(window_name, img, max_width=800, max_height=600):
    """Resize image to fit within (max_width, max_height) while keeping aspect ratio."""
    h, w = img.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)  # only scale down
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    cv2.imshow(window_name, resized)

def overlay_filled_contours(image, contours, roi=None, alpha=0.5, random_colors=True):
    """
    Overlay filled contour regions (colored) on top of the original image.
    Each contour can be assigned a different color.

    Args:
        image (np.ndarray): Original BGR image.
        contours (list): Contours detected (possibly from ROI area).
        roi (tuple[int,int,int,int], optional): (x, y, w, h) ROI offset if contours are from cropped region.
        alpha (float): Transparency level (0–1).
        random_colors (bool): If True, uses a random color for each contour.

    Returns:
        np.ndarray: Image with filled contour overlay.
    """
    overlay = image.copy()
    fill_layer = np.zeros_like(image, dtype=np.uint8)

    # Shift contours if they came from cropped ROI
    if roi is not None:
        x, y, w, h = roi
        shifted_contours = [c + [x, y] for c in contours]
    else:
        shifted_contours = contours

    # Assign and draw colors
    for i, contour in enumerate(shifted_contours):
        if random_colors:
            # Random bright color
            color = tuple(np.random.randint(80, 255, 3).tolist())
        else:
            # Cycle through predefined colors
            colors = [
                (0, 255, 0),   # Green
                (255, 0, 0),   # Blue
                (0, 0, 255),   # Red
                (0, 255, 255), # Yellow
                (255, 0, 255), # Magenta
                (255, 255, 0)  # Cyan
            ]
            color = colors[i % len(colors)]

        cv2.drawContours(fill_layer, [contour], -1, color, thickness=cv2.FILLED)

    # Blend overlay
    blended = cv2.addWeighted(image, 1 - alpha, fill_layer, alpha, 0)
    return blended
