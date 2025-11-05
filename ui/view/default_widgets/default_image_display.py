from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from ui.model.image_model import ImageModel 
import os
class DefaultImageDisplay(QWidget):
    """
    Simple bordered image container with an internal title bar.
    Shows 'No Image Loaded' if no image is provided.
    """

    def __init__(self, parent=None, model : ImageModel = None, title="Image"):
        super().__init__(parent)
        self.model = model if model is not None else ImageModel()

        # === Outer container styling ===
        self.setObjectName("DefaultImageDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #DefaultImageDisplay {
                background-color: #2b2b2b;
                border: 1px solid #555;
                border-radius: 8px;
            }
        """)

        # === Title bar (inside the container) ===
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

        # === Image display area ===
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #1e1e1e;
            color: #aaaaaa;
            border: none;
        """)

        # === Layout setup ===
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label, stretch=1)

        # === Optional: initial image ===
        self.update_image_view()

    def update_image_view(self):
        """Show image if exists, otherwise show placeholder text."""
        print(f"updating image view... {self.model.image}")
        if self.model.image and os.path.exists(self.model.image):
            print("image path exists...")
            pixmap = QPixmap(self.model.image)
            if not pixmap.isNull():
                print("setting pixmap...")
                self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
                return
        # fallback: no valid image
        self.image_label.setText("No image")
