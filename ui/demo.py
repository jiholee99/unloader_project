from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout

class RatioWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main vertical layout (button + content)
        main_layout = QVBoxLayout(self)

        # Create button
        self.button = QPushButton("Switch Ratio")
        self.button.clicked.connect(self.switch_ratio)

        # Content layout (horizontal)
        self.h_layout = QHBoxLayout()

        # Three widgets
        self.w1 = QLabel("A")
        self.w2 = QLabel("B")
        self.w3 = QLabel("C")

        # Give each widget a background color
        self.w1.setStyleSheet("background-color: #FF9999; font-size: 24px;")
        self.w2.setStyleSheet("background-color: #99FF99; font-size: 24px;")
        self.w3.setStyleSheet("background-color: #9999FF; font-size: 24px;")

        # Center text
        self.w1.setAlignment(Qt.AlignCenter)
        self.w2.setAlignment(Qt.AlignCenter)
        self.w3.setAlignment(Qt.AlignCenter)

        # Add widgets
        self.h_layout.addWidget(self.w1)
        self.h_layout.addWidget(self.w2)
        self.h_layout.addWidget(self.w3)

        # Default 3:3:3 ratio
        self.h_layout.setStretch(0, 3)
        self.h_layout.setStretch(1, 3)
        self.h_layout.setStretch(2, 3)

        # Add layouts
        main_layout.addWidget(self.button)
        main_layout.addLayout(self.h_layout)

        # Toggle state
        self.state = 0

    def switch_ratio(self):
        if self.state == 0:
            # Switch to 6:1:1 ratio
            self.h_layout.setStretch(0, 6)
            self.h_layout.setStretch(1, 1)
            self.h_layout.setStretch(2, 1)
            self.state = 1
        else:
            # Back to 3:3:3
            self.h_layout.setStretch(0, 3)
            self.h_layout.setStretch(1, 3)
            self.h_layout.setStretch(2, 3)
            self.state = 0


if __name__ == "__main__":
    from PySide6.QtCore import Qt
    app = QApplication([])
    window = RatioWindow()
    window.resize(900, 300)
    window.show()
    app.exec()
