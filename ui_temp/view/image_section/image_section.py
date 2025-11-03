from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .image_viewer import ImageViewer  # your existing class
from ..config.theme import Theme

class ImageSection(QWidget):
    def __init__(self):
        super().__init__()

        # Give this widget a unique ID
        self.setObjectName("ImageSection")

        outer_layout = QVBoxLayout(self)

        # Inner frame
        self.frame = QFrame()
        self.frame.setObjectName("InnerFrame")
        # Set padding and style for the inner frame
        self.frame.setStyleSheet(f"""
            #InnerFrame {{
                background-color: {Theme.overlay_background_color};
                border-radius: 8px;
            }}
        """)

        inner_layout = QVBoxLayout(self.frame)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        inner_layout.setSpacing(5)

        # Title
        self.title = QLabel("Image")
        self.title.setFont(QFont("Arial", 12, QFont.Bold))
        self.title.setAlignment(Qt.AlignLeft)

        # Image viewer
        self.viewer = ImageViewer()

        inner_layout.addWidget(self.title)
        inner_layout.addWidget(self.viewer)
        outer_layout.addWidget(self.frame)

    def show_image(self, img):
        self.viewer.show_image(img)
