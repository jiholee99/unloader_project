from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from ..config.theme import Theme


class DefaultScrollView(QWidget):
    """
    A reusable, scrollable text display box with dark rounded styling.
    Example:
        scroll_view = DefaultScrollView("This is long text...")
    """

    def __init__(self, text: str = "", parent=None):
        super().__init__(parent)

        # === Layout ===
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # === Scroll Area (main container) ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)

        # Apply modern dark style
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: "#2e2e2e";
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}

            /* Scrollbar styling */
            QScrollBar:vertical {{
                background: {Theme.content_container_color};
                width: 10px;
                margin: 4px 0 4px 0;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #555;
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Theme.primary_color};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

        # === Content widget inside scroll area ===
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)

        # === Label for text ===
        self.label = QLabel(text)
        self.label.setStyleSheet("color: white; font-size: 13px;")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        content_layout.addWidget(self.label)
        self.scroll_area.setWidget(content_widget)
        layout.addWidget(self.scroll_area)

        self.setLayout(layout)

    def set_text(self, text: str):
        """Update the displayed text dynamically."""
        self.label.setText(text)

    def append_text(self, new_line: str):
        """Append new text with a newline (useful for logs)."""
        current = self.label.text()
        self.label.setText(current + "\n" + new_line)
        self.label.adjustSize()
