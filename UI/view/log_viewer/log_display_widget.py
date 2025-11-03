from PySide6.QtWidgets import QWidget, QVBoxLayout
from ..config.theme import Theme
from ..default_widgets.default_scrollview import DefaultScrollView


class LogDisplayWidget(QWidget):
    """
    Log display area with a dark scrollable text box.
    """
    def __init__(self, parent=None, text="Initializing log viewer..."):
        super().__init__(parent)

        # === Main Layout ===
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)


        # === Scrollable Text View ===
        sample_text = "sdasd\nsadasd\nsadasdasd\nsadsadsd" # Sample long text for demonstration
        self.scroll_view = DefaultScrollView(sample_text)
        layout.addWidget(self.scroll_view)

        self.setLayout(layout)

    # Optional: Add helper methods for convenience
    def append_log(self, message: str):
        """Add a new line to the log."""
        self.scroll_view.append_text(message)

    def set_log(self, text: str):
        """Replace the log text."""
        self.scroll_view.set_text(text)
