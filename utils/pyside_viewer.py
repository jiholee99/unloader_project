# utils/pyside_multi_viewer.py

import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QObject, Signal, Slot

_viewer = None  # Singleton instance


# ==============================================================
# SIGNAL BUS (Used to safely update UI from worker threads)
# ==============================================================
class ImageUpdateSignal(QObject):
    update = Signal(str, object)  # (image_id, cv_img)


signal_bus = ImageUpdateSignal()


# ==============================================================
# MAIN VIEWER CLASS
# ==============================================================
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multi Image Viewer")
        self.resize(1200, 900)

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Maps image_id → {"title": QLabel, "image": QLabel}
        self.items = {}

        # Connect signal from worker threads to UI update slot
        signal_bus.update.connect(self._update_image_slot)

    # ----------------------------------------------------------
    # PUBLIC: initialize predefined slots
    # ----------------------------------------------------------
    def initialize_slots(self, ids):
        """
        Pre-create empty slots so show_image(id) won't crash.
        """
        for image_id in ids:
            if image_id not in self.items:
                self._create_item(image_id)

        self._refresh_grid()

    # ----------------------------------------------------------
    # PUBLIC: thread-safe add/update
    # ----------------------------------------------------------
    def add_image(self, image_id: str, cv_img=None):
        """
        Thread-safe. cv_img may be None — ignored until later.
        """
        signal_bus.update.emit(image_id, cv_img)

    def show_image(self, image_id: str, cv_img=None):
        self.add_image(image_id, cv_img)

    # ----------------------------------------------------------
    # INTERNAL: Create UI container for a given image ID
    # ----------------------------------------------------------
    def _create_item(self, image_id):
        title = QLabel(image_id, alignment=Qt.AlignCenter)
        title.setStyleSheet("background-color: #333; color: white; padding: 5px;")

        image_label = QLabel("No Image", alignment=Qt.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label.setStyleSheet("background-color: #111; color: #777; padding: 10px;")
        image_label.setMinimumSize(320, 240)

        container = QVBoxLayout()
        container_widget = QWidget()
        container_widget.setLayout(container)

        container.addWidget(title)
        container.addWidget(image_label)

        self.items[image_id] = {
            "container": container_widget,
            "title": title,
            "image": image_label,
        }

        return container_widget

    # ----------------------------------------------------------
    # INTERNAL: UI update slot (runs only in Qt main thread)
    # ----------------------------------------------------------
    @Slot(str, object)
    def _update_image_slot(self, image_id, cv_img):
        """
        UI-safe slot. Updates QLabel with new image.
        Supports grayscale and BGR images.
        """

        # Create container if needed
        if image_id not in self.items:
            self._create_item(image_id)
            self._refresh_grid()

        image_label = self.items[image_id]["image"]

        # If no image given → do nothing
        if cv_img is None:
            return

        # Ensure contiguous memory
        cv_img = np.ascontiguousarray(cv_img)

        # Convert image
        if cv_img.ndim == 2:  # Gray
            h, w = cv_img.shape
            qimg = QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)

        elif cv_img.ndim == 3 and cv_img.shape[2] == 3:  # BGR → RGB
            rgb = cv_img[:, :, ::-1]
            rgb = np.ascontiguousarray(rgb)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        else:
            print("Unsupported image format:", cv_img.shape)
            return

        # Scale and show
        pix = QPixmap.fromImage(qimg)
        pix = pix.scaled(image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pix)

    # ----------------------------------------------------------
    # INTERNAL: redraw the grid
    # ----------------------------------------------------------
    def _refresh_grid(self):
        # Clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Add items row-by-row
        containers = [v["container"] for v in self.items.values()]
        cols = 3

        for i, widget in enumerate(containers):
            r = i // cols
            c = i % cols
            self.grid.addWidget(widget, r, c)


# ==============================================================
# SINGLETON ACCESSOR
# ==============================================================
def start_image_viewer():
    """
    Creates the viewer window if needed and returns it.
    QApplication MUST already be created in main.py.
    """
    global _viewer

    if _viewer is None:
        _viewer = ImageViewer()
        _viewer.show()

    return _viewer
