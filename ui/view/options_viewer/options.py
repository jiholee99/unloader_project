from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from ui.view.default_widgets.default_button import DefaultButton

class Options(QWidget):
    button1_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        button = DefaultButton("Load Image")
        layout.addWidget(button)
        button2 = DefaultButton("Option 2")
        layout.addWidget(button2)

        button.clicked.connect(self.button1_clicked.emit)