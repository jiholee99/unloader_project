from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from ui.view.config.theme import Theme

class Appbar(QWidget):
    def __init__(self):
        super().__init__()

        # Give this widget a unique ID
        self.setObjectName("Appbar")

        self.setStyleSheet(f"""
            #Appbar {{
                background-color: {Theme.primary_dark};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        # You can add buttons or labels to the appbar here
        self.title = QLabel("MVC Image Processor")
        self.title.setStyleSheet(f"color: {Theme.text_color}; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title, alignment=Qt.AlignLeft)
        # Add more widgets like buttons as needed
        self.setLayout(layout)

    