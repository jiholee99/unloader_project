from ..config.theme import Theme
from PySide6.QtWidgets import QPushButton

class DefaultButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"background-color: {Theme.primary_color}; color: white; hover {{ background-color: #005f99; }}")
