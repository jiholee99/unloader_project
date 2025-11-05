from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from ui.view.options_viewer.options_viewer_widget import OptionsViewer
from ui.view.image_viewer.image_viewer_widget import ImageViewerWidget
from ui.view.config.theme import Theme
from ui.view.log_viewer.log_viewer_widget import LogViewerWidget
from ui.view.appbar.appbar_widget import Appbar
from utils.logger import get_logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC Image Processor")
        self.resize(1300, 700)

        self.setStyleSheet(f"""
            #MainWindow {{
                background-color: {Theme.background_color};
            }}
        """)
        get_logger().info("MainWindow initialized.")
        # Main background color
        self.setObjectName("MainWindow")

        # Column first : App bar and main panel
        self.appbar = Appbar()
        self.appbar.setFixedHeight(50)

        layout = QVBoxLayout()
        layout.addWidget(self.appbar)

        # Main Panel layout : Side panel on left, image viewer and log on right (vertically)

        self.options_viewer = OptionsViewer()
        # self.side_panel.setStyleSheet(f"background-color: {Theme.overlay_background_color}; border-radius: 15px;")
        self.options_viewer.setContentsMargins(0,0,0,0)
        self.image_viewer = ImageViewerWidget()
        self.log_viewer = LogViewerWidget()

        self.main_panel_layout = QHBoxLayout()
        self.main_panel_layout.setContentsMargins(0,0,0,0)
        self.main_panel_layout.addWidget(self.options_viewer)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_viewer, stretch=4)
        right_layout.addWidget(self.log_viewer, stretch=1)
        self.main_panel_layout.addLayout(right_layout, stretch=5)
        self.main_panel = QWidget()
        self.main_panel.setLayout(self.main_panel_layout)
        layout.addWidget(self.main_panel)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
