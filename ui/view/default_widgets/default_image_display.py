from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QWheelEvent
import numpy as np


class DefaultImageDisplay(QWidget):
    """
    Fast bordered image container for OpenCV (NumPy) images.
    - Accepts only NumPy arrays (BGR, RGB, RGBA, or Grayscale)
    - Auto-resizes to fit container
    - Supports zoom in/out (Ctrl + wheel)
    """

    def __init__(self, parent=None, title="Image"):
        super().__init__(parent)
        self._pixmap = None
        self._zoom_factor = 1.0

        # === Styling ===
        self.setObjectName("DefaultImageDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #DefaultImageDisplay {
                background-color: #2b2b2b;
                border: 1px solid #555;
                border-radius: 8px;
            }
        """)

        # === Title ===
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            background-color: #3c3c3c;
            color: #ffffff;
            font-size: 12px;
            padding: 4px;
            border-bottom: 1px solid #555;
            border-top-left-radius: 7px;
            border-top-right-radius: 7px;
        """)

        # === Image area ===
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #1e1e1e;
            color: #aaaaaa;
            border: none;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label, stretch=1)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def update_image_view(self, cv_img: np.ndarray | None):
        """Display an OpenCV (NumPy) image."""
        if cv_img is None or not isinstance(cv_img, np.ndarray):
            self._pixmap = None
            self.image_label.setText("No Image Loaded")
            return

        try:
            self._pixmap = self._cv2_to_pixmap(cv_img)
        except Exception as e:
            print(f"[DefaultImageDisplay] Error converting OpenCV image: {e}")
            self.image_label.setText("Invalid Image")
            self._pixmap = None
            return

        if self._pixmap and not self._pixmap.isNull():
            self._zoom_factor = 1.0
            self._update_scaled_image()
        else:
            self.image_label.setText("Invalid Image")

    def zoom_in(self, factor=1.25):
        if self._pixmap:
            self._zoom_factor *= factor
            self._update_scaled_image()

    def zoom_out(self, factor=1.25):
        if self._pixmap:
            self._zoom_factor /= factor
            self._update_scaled_image()

    # -------------------------------------------------------------------------
    # Internal logic
    # -------------------------------------------------------------------------

    def _cv2_to_pixmap(self, cv_img: np.ndarray) -> QPixmap:
        if cv_img is None or not isinstance(cv_img, np.ndarray):
            raise ValueError("Invalid OpenCV image input")

        # Enforce contiguous, aligned, 8-bit
        cv_img = np.ascontiguousarray(cv_img, dtype=np.uint8).copy(order='C')

        if cv_img.ndim == 2:
            h, w = cv_img.shape
            qimage = QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)

        elif cv_img.ndim == 3:
            h, w, ch = cv_img.shape
            if ch == 3:
                cv_img = cv_img[:, :, ::-1].copy(order='C')  # BGR → RGB, make aligned copy
                bytes_per_line = 3 * w
                qimage = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            elif ch == 4:
                cv_img = cv_img[:, :, [2, 1, 0, 3]].copy(order='C')
                bytes_per_line = 4 * w
                qimage = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
            else:
                raise ValueError(f"Unsupported number of channels: {ch}")
        else:
            raise ValueError("Invalid image dimensions")

        # Make sure Qt owns the buffer independently
        return QPixmap.fromImage(qimage.copy())


    def _update_scaled_image(self):
        """Scale the pixmap to fit container + zoom factor."""
        if not self._pixmap:
            return

        container_size = self.image_label.size()
        scaled_size = QSize(
            int(container_size.width() * self._zoom_factor),
            int(container_size.height() * self._zoom_factor),
        )

        scaled_pixmap = self._pixmap.scaled(
            scaled_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled_image()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in(1.1)
            else:
                self.zoom_out(1.1)
            event.accept()
        else:
            super().wheelEvent(event)
