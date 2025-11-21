import sys
import cv2
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QSlider
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QImage


def to_pixmap(img) -> QPixmap:
    """Convert numpy/OpenCV image to QPixmap."""
    h, w = img.shape[:2]
    if img.ndim == 2:
        qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
    else:
        qimg = QImage(img.data, w, h, img.strides[0], QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)


class ScaledImageView(QLabel):
    """A QLabel that automatically scales the pixmap to fill the widget."""

    def __init__(self):
        super().__init__()
        self._pixmap = None
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background:#222; border:1px solid gray;")

    def set_image(self, pixmap: QPixmap):
        """Set image and trigger repaint."""
        self._pixmap = pixmap
        self.update()

    def resizeEvent(self, event):
        """Re-scale on every resize."""
        self.update()

    def paintEvent(self, event):
        """Custom paint to auto-scale pixmap."""
        if self._pixmap:
            scaled = self._pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            painter = QtGui.QPainter(self)
            painter.drawPixmap(
                (self.width() - scaled.width()) // 2,
                (self.height() - scaled.height()) // 2,
                scaled
            )
        else:
            super().paintEvent(event)


class ThresholdView(QWidget):
    threshold_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.image_view = ScaledImageView()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.setValue(128)

        layout = QVBoxLayout()
        layout.addWidget(self.image_view)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.threshold_changed)


class ThresholdController:
    def __init__(self, view):
        self.view = view

        # Load a sample image
        test_path = r"assets\test_images\full.jpeg"  # change path
        self.original = cv2.cvtColor(cv2.imread(test_path), cv2.COLOR_BGR2RGB)

        view.threshold_changed.connect(self.apply_threshold)
        self.apply_threshold(view.slider.value())

    def apply_threshold(self, value):
        gray = cv2.cvtColor(self.original, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)

        pix = to_pixmap(mask)
        self.view.image_view.set_image(pix)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.view = ThresholdView()
        self.ctrl = ThresholdController(self.view)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


if __name__ == "__main__":
    from PySide6 import QtGui  # needed for QPainter
    app = QApplication(sys.argv)
    window = App()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
