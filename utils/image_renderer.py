# utils/image_renderer.py

import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt


class ImageRenderer:
    """Handles OpenCV → Qt image conversions."""

    @staticmethod
    def cv_to_qimage(cv_img):
        if cv_img is None:
            return None

        cv_img = np.ascontiguousarray(cv_img)

        # grayscale
        if cv_img.ndim == 2:
            h, w = cv_img.shape
            return QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)

        # BGR → RGB
        if cv_img.ndim == 3 and cv_img.shape[2] == 3:
            rgb = cv_img[:, :, ::-1]
            rgb = np.ascontiguousarray(rgb)
            h, w, ch = rgb.shape
            return QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)

        print("Unsupported image format:", cv_img.shape)
        return None

    @staticmethod
    def scale_for_label(qimage, label):
        if qimage is None:
            return None
        pix = QPixmap.fromImage(qimage)
        return pix.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
