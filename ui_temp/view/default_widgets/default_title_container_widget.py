from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from ..default_widgets.default_button import DefaultButton

class DefaultContainerTitleWidget(QWidget):
    def __init__(self, parent=None, title="Default Title Fullview Widget"):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.setObjectName("DefaultTitleFullviewWidget")
        self.setLayout(self.layout)

        # Title
        self.title = QLabel(title)
        self.setStyleSheet("#DefaultTitleFullviewWidget QLabel { font-size: 16px; font-weight: bold; }")
        self.layout.addWidget(self.title)

