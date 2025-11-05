from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from ui.view.config.theme import Theme


class DefaultScrollView(QScrollArea):
    """
    A reusable scrollable container for any QWidget.
    Automatically handles resizing, scrollbars, and styling.
    """

    def __init__(self, child_widget: QWidget = None, parent=None):
        super().__init__(parent)

        # Scroll behavior
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QScrollArea.NoFrame)

        self.child_widget = child_widget


        # Force a background on *viewport* to remove dotted transparency
        self.viewport().setStyleSheet(f"background-color: {Theme.background_color}; border: none;")

        # Style (dark theme)
        self.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Theme.background_color};
                border: none;
            }}

        """)

        # Create inner container
        container = QWidget()
        container.setStyleSheet(f"background-color: {Theme.background_color};")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # Add child widget if given
        if child_widget:
            layout.addWidget(child_widget)

        self.setWidget(container)
