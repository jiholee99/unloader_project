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
    Overlay filled contour regions (colored) on top of the original image,
    with LARGE indexed numbers displayed on top of each contour with background.
    """
    overlay = image.copy()
    fill_layer = np.zeros_like(image, dtype=np.uint8)

    # Shift contours if ROI used
    if roi is not None:
        x_offset, y_offset, _, _ = roi
        shifted_contours = [c + [x_offset, y_offset] for c in contours]
    else:
        shifted_contours = contours

    for i, contour in enumerate(shifted_contours):

        # Pick contour color
        if random_colors:
            color = tuple(np.random.randint(80, 255, 3).tolist())
        else:
            predefined = [
                (0, 255, 0), (255, 0, 0), (0, 0, 255),
                (0, 255, 255), (255, 0, 255), (255, 255, 0)
            ]
            color = predefined[i % len(predefined)]

        # Draw contour fill
        cv2.drawContours(fill_layer, [contour], -1, color, thickness=cv2.FILLED)

        # Compute centroid
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = x + w // 2, y + h // 2

        # ================================
        # LARGE TEXT + BACKGROUND BOX
        # ================================
        text = str(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.5        # EXTRA LARGE
        thickness = 6           # Thick stroke for visibility

        # Get text size
        (tw, th), baseline = cv2.getTextSize(text, font, font_scale, thickness)

        # Background rectangle coordinates
        x1 = cx - tw // 2 - 10
        y1 = cy - th // 2 - 10
        x2 = cx + tw // 2 + 10
        y2 = cy + th // 2 + 10

        # Draw dark background box (semi-transparent effect done by blending later)
        cv2.rectangle(fill_layer, (x1, y1), (x2, y2), (0, 0, 0), cv2.FILLED)

        # Draw white text on top
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

    # Blend overlay with original image
    blended = cv2.addWeighted(image, 1 - alpha, fill_layer, alpha, 0)
    return blended


