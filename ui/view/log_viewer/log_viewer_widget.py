from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from ui.view.default_widgets.default_title_container_widget import DefaultContainerTitleWidget
from ui.view.config.theme import Theme
from .log_display_widget import LogDisplayWidget
from ui.view.default_widgets.default_viewer_container_widget import DefaultViewerContainerWidget

class LogViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.log_display = LogDisplayWidget()

        # Wrap it inside the reusable container
        container = DefaultViewerContainerWidget(
            title="Log Viewer",
            child_widget=self.log_display
        )

        # Now make 'outer' the only thing inside self.layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(150)
        self.setMinimumWidth(300)


