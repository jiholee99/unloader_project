from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from ..default_widgets.default_title_container_widget import DefaultContainerTitleWidget
from ..config.theme import Theme
from .log_display_widget import LogDisplayWidget
class LogViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QWidget()
        # outer.setAttribute(Qt.WA_StyledBackground, True)
        outer.setObjectName("LogViewerWidget")
        outer.setStyleSheet(f"""
            #LogViewerWidget {{
                background-color: {Theme.overlay_background_color};
                border-radius: 15px;
            }}
        """)

        outer.setContentsMargins(5, 5, 5, 5)

        # Outer layer is the container with rounded corners. title and log display here
        outer_layout = QVBoxLayout(outer)

        self.title_fullview_widget = DefaultContainerTitleWidget(title="Log Viewer")
        outer_layout.addWidget(self.title_fullview_widget)

        self.log_display = LogDisplayWidget()
        outer_layout.addWidget(self.log_display, stretch=1)

        # Now make 'outer' the only thing inside self.layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(outer)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(150)
        self.setMinimumWidth(300)


