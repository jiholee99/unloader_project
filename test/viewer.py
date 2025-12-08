import sys
import cv2
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QImage, QPixmap


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")

        self.images = []  # history if needed
        self.label = QLabel()
        self.label.setFixedSize(640, 480)

        # Buttons (optional)
        btn_load = QPushButton("Load Image (Demo)")
        btn_load.clicked.connect(self.gui_load_image)

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(btn_load)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(layout_btn)
        self.setLayout(layout)

    # -------------------------------------------------------
    # ONE FUNCTION YOU CALL → show_image(cv_img)
    # -------------------------------------------------------
    def show_image(self, cv_img):
        """Stores and displays a cv2 BGR image."""
        if cv_img is None:
            return

        self.images.append(cv_img)

        h, w, ch = cv_img.shape
        bytes_per_line = ch * w

        q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    # Demo loader
    def gui_load_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Image")
        if file:
            cv_img = cv2.imread(file)
            self.show_image(cv_img)


# ------------------------------------------------------------
# Single entry point — call start_image_viewer() anywhere
# ------------------------------------------------------------
_qapp = None
_viewer = None


def start_image_viewer():
    """
    Starts QApplication and returns viewer instance.
    You then call: viewer.show_image(cv_img)
    """
    global _qapp, _viewer

    if _qapp is None:
        _qapp = QApplication(sys.argv)

    if _viewer is None:
        _viewer = ImageViewer()
        _viewer.show()

    return _viewer


# Standalone run
if __name__ == "__main__":
    viewer = start_image_viewer()
    sys.exit(_qapp.exec())
