from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
from ..config.theme import Theme
from ..default_widgets.default_button import DefaultButton

class SidePanel(QWidget):
    load_image_clicked = Signal()
    process_clicked = Signal()
    quit_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)

        self.btn_load = QPushButton("Load Image")
        self.btn_process = QPushButton("Threshold")
        self.btn_quit = QPushButton("Quit")

        layout = QVBoxLayout()
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_process)
        layout.addWidget(self.btn_quit)
        layout.addStretch()
        self.setLayout(layout)

        self.btn_load.clicked.connect(self.load_image_clicked.emit)
        self.btn_process.clicked.connect(self.process_clicked.emit)
        self.btn_quit.clicked.connect(self.quit_clicked.emit)
