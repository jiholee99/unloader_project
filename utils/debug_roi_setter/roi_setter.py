import sys
import cv2
import json
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen
from PySide6.QtCore import Qt, QRect


class ImageLabel(QLabel):
    """Interactive QLabel to select ROI with correct coordinate mapping."""
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #333;")
        self.pixmap_image = None
        self.display_pixmap = None
        self.start_point = None
        self.end_point = None
        self.roi_rect = None
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def set_image(self, image):
        """Store original image and show scaled version."""
        self.original_image = image
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qimg = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
        self.pixmap_image = QPixmap.fromImage(qimg)

        # Scale pixmap to fit label
        display_pix = self.pixmap_image.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.display_pixmap = display_pix
        self.setPixmap(display_pix)

        # Calculate scale and offset for coordinate mapping
        self.scale_x = w / display_pix.width()
        self.scale_y = h / display_pix.height()
        self.offset_x = (self.width() - display_pix.width()) // 2
        self.offset_y = (self.height() - display_pix.height()) // 2

    def mousePressEvent(self, event):
        if not self.display_pixmap:
            return
        pos = event.position().toPoint()
        if not self._in_display_area(pos):
            return
        self.start_point = pos
        self.end_point = pos
        self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            pos = event.position().toPoint()
            if self._in_display_area(pos):
                self.end_point = pos
                self.update()

    def mouseReleaseEvent(self, event):
        if self.start_point and self.end_point:
            self.end_point = event.position().toPoint()
            self.roi_rect = QRect(self.start_point, self.end_point).normalized()
            self.update()
            print(f"ROI (display): {self.roi_rect.x()}, {self.roi_rect.y()}, "
                  f"{self.roi_rect.width()}, {self.roi_rect.height()}")
        self.start_point = None
        self.end_point = None

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.display_pixmap and (self.start_point or self.roi_rect):
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 2, Qt.DashLine))
            if self.start_point and self.end_point:
                painter.drawRect(QRect(self.start_point, self.end_point))
            elif self.roi_rect:
                painter.drawRect(self.roi_rect)

    def _in_display_area(self, pos):
        return (
            self.offset_x <= pos.x() <= self.offset_x + self.display_pixmap.width()
            and self.offset_y <= pos.y() <= self.offset_y + self.display_pixmap.height()
        )

    def get_roi_from_original(self):
        """Return cropped ROI and coordinates in original image coordinates."""
        if not self.roi_rect or not hasattr(self, "original_image"):
            return None, None

        x = int((self.roi_rect.x() - self.offset_x) * self.scale_x)
        y = int((self.roi_rect.y() - self.offset_y) * self.scale_y)
        w = int(self.roi_rect.width() * self.scale_x)
        h = int(self.roi_rect.height() * self.scale_y)

        x = max(0, x)
        y = max(0, y)
        w = min(self.original_image.shape[1] - x, w)
        h = min(self.original_image.shape[0] - y, h)

        roi = self.original_image[y:y+h, x:x+w]
        coords = {"x": x, "y": y, "w": w, "h": h}
        print(f"ROI (original): {coords}")
        return roi, coords


class ROIDebugger(QWidget):
    def __init__(self, save_path="config/app_config.json"):
        super().__init__()
        self.setWindowTitle("ROI Debug Tool with Save (JSON)")
        self.resize(1000, 800)

        self.save_path = save_path
        self.image_label = ImageLabel()
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        self.save_button = QPushButton("Save ROI to JSON")
        self.save_button.clicked.connect(self.save_roi)

        self.roi_preview = QLabel("ROI Preview")
        self.roi_preview.setAlignment(Qt.AlignCenter)
        self.roi_preview.setStyleSheet("background-color: #222; color: #ccc;")
        self.roi_preview.setFixedSize(300, 300)

        layout = QHBoxLayout()
        layout.addWidget(self.image_label)
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.load_button)
        right_panel.addWidget(self.roi_preview)
        right_panel.addWidget(self.save_button)
        layout.addLayout(right_panel)
        self.setLayout(layout)

        self.image_label.mouseReleaseEvent = self._roi_released
        self.last_coords = None

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.jpg *.png *.jpeg *.bmp)"
        )
        if not path:
            return
        image = cv2.imread(path)
        if image is None:
            QMessageBox.warning(self, "Error", "❌ Failed to load image.")
            return
        self.image_label.set_image(image)

    def _roi_released(self, event):
        ImageLabel.mouseReleaseEvent(self.image_label, event)
        roi, coords = self.image_label.get_roi_from_original()
        if roi is not None and roi.size > 0:
            self.last_coords = coords
            roi_resized = cv2.resize(roi, (300, 300), interpolation=cv2.INTER_AREA)
            h, w, ch = roi_resized.shape
            qimg = QImage(roi_resized.data, w, h, ch * w, QImage.Format_BGR888)
            self.roi_preview.setPixmap(QPixmap.fromImage(qimg))
        else:
            self.roi_preview.setText("Invalid ROI")

    def save_roi(self):
        """Save or update ROI coordinates in appconfig.json."""
        if not self.last_coords:
            QMessageBox.information(self, "No ROI", "No ROI selected to save.")
            return

        data = {}
        try:
            # Load existing JSON if it exists
            with open(self.save_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            pass  # If file doesn't exist, start fresh
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "⚠️ Invalid JSON, overwriting file.")

        # Update or add ROI key
        data["roi"] = self.last_coords

        try:
            with open(self.save_path, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Saved", f"ROI updated in:\n{self.save_path}")
            print(f"✅ ROI saved to {self.save_path}: {data}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save ROI:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ROIDebugger(save_path="config/app_config.json")
    win.show()
    sys.exit(app.exec())
