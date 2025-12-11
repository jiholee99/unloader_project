import cv2
import numpy as np
from model.contour import Contour
def show_scaled(window_name, img, max_width=800, max_height=600):
    """Resize image to fit within (max_width, max_height) while keeping aspect ratio."""
    h, w = img.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)  # only scale down
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    cv2.imshow(window_name, resized)

def overlay_filled_contours(image, contour_objs : list[Contour], roi=None, alpha=0.5):
    """
    Draw filled contour overlays using the color stored in each Contour object.

    Args:
        image: input BGR image
        contour_objs: list of Contour objects
        roi: (x, y, w, h) if contours came from cropped region
        alpha: transparency level for blending
    """
    overlay = image.copy()
    fill_layer = np.zeros_like(image, dtype=np.uint8)

    # ROI offset shifting
    if roi is not None:
        x_offset, y_offset, _, _ = roi
    else:
        x_offset, y_offset = 0, 0

    for i, c_obj in enumerate(contour_objs):

        contour = c_obj.contour

        # Apply ROI shift if needed
        contour_shifted = contour + [x_offset, y_offset]

        # ============================================
        # USE Contour object's assigned human color
        # c_obj.color is a tuple: (name, (B,G,R))
        # ============================================
        _, (r, g, b) = c_obj.color
        color = (b, g, r)   # convert RGB → BGR for OpenCV

        # Draw filled contour
        cv2.drawContours(fill_layer, [contour_shifted], -1, color, thickness=cv2.FILLED)

        # Compute centroid
        M = cv2.moments(contour_shifted)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            x, y, w, h = cv2.boundingRect(contour_shifted)
            cx, cy = x + w // 2, y + h // 2

        # =====================================
        # INDEX NUMBER WITH DARK BACKGROUND BOX
        # =====================================
        text = str(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.5
        thickness = 6

        (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        x1 = cx - tw // 2 - 10
        y1 = cy - th // 2 - 10
        x2 = cx + tw // 2 + 10
        y2 = cy + th // 2 + 10

        # black box
        cv2.rectangle(fill_layer, (x1, y1), (x2, y2), (0, 0, 0), cv2.FILLED)

        # white number
        cv2.putText(
            fill_layer,
            text,
            (cx - tw // 2, cy + th // 2),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )

    # Blend overlay with original frame
    blended = cv2.addWeighted(image, 1 - alpha, fill_layer, alpha, 0)
    return blended



