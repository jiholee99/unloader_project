from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from ..config.theme import Theme
import cv2

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"background-color: {Theme.background_color}; color: gray;")
        self.setText("No image loaded")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def show_image(self, img):
        if img is None:
            self.setText("Invalid image")
            return

        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0],
                          img_rgb.strides[0], QImage.Format_RGB888)
        else:
            qimg = QImage(img.data, img.shape[1], img.shape[0],
                          img.strides[0], QImage.Format_Grayscale8)

        pix = QPixmap.fromImage(qimg).scaled(
            self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setPixmap(pix)
        self.setText("")
