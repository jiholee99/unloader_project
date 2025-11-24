import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QMainWindow
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QPointF


class ZoomPanImageView(QGraphicsView):
    def __init__(self, image: np.ndarray):
        super().__init__()

        # --- Convert NumPy → QPixmap ---
        if image.ndim == 2:
            qimg = QImage(
                image.data, image.shape[1], image.shape[0],
                image.shape[1], QImage.Format_Grayscale8
            )
        else:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimg = QImage(
                rgb.data, rgb.shape[1], rgb.shape[0],
                rgb.shape[1] * 3, QImage.Format_RGB888
            )

        pixmap = QPixmap.fromImage(qimg)

        # --- Scene Setup ---
        self.scene = QGraphicsScene(self)
        self.pix_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pix_item)
        self.setScene(self.scene)

        # --- View Setup ---
        self.setRenderHints(self.renderHints())
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # ← enables panning
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # zoom to cursor
        self.scale_factor = 1.0

    # --- Zoom with wheel ---
    def wheelEvent(self, event):
        zoom_in_factor = 1.2
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

    # --- Right click resets view ---
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.resetTransform()
            return
        super().mousePressEvent(event)


# =================================================================
# Simple popup window wrapper
# =================================================================
class DebugImageViewer:
    @staticmethod
    def show(image: np.ndarray):
        app = QApplication.instance()
        created = False

        if app is None:
            app = QApplication(sys.argv)
            created = True

        win = QMainWindow()
        win.setWindowTitle("Zoom + Pan Image Viewer")
        view = ZoomPanImageView(image)
        win.setCentralWidget(view)
        win.resize(1200, 800)
        win.show()

        if created:
            sys.exit(app.exec())
