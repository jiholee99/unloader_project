from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from ui.view.default_widgets.default_title_container_widget import DefaultContainerTitleWidget
from ui.view.config.theme import Theme

class DefaultViewerContainerWidget(QWidget):
    """
    A reusable rounded container with overlay background and title.
    The title stays at the top; the child widget expands to fill space.
    """
    def __init__(self, title: str, child_widget: QWidget, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("DefaultViewerContainerWidget")
        self.setStyleSheet(f"""
            #DefaultViewerContainerWidget {{
                background-color: {Theme.overlay_background_color};
                border-radius: 15px;
            }}
        """)

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Title (fixed size at top)
        self.title_widget = DefaultContainerTitleWidget(title=title)
        self.title_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.title_widget, alignment=Qt.AlignTop)

        # Child widget should expand to fill remaining space
        child_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(child_widget)

        # Make the whole container expandable
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
