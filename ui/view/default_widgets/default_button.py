from ..config.theme import Theme
from PySide6.QtWidgets import QPushButton

class DefaultButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("DefaultButton")
        self.setStyleSheet(f"""
            #DefaultButton {{
                background-color: {Theme.primary_color};
                color: {Theme.text_color};
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
            }}
            #DefaultButton:hover {{
                background-color: #005f99;
            }}
        """)
