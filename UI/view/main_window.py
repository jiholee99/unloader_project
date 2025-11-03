from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from ui.view.side_panel.side_panel import SidePanel
from ui.view.image_section.image_section import ImageSection
from ui.view.config.theme import Theme
from ui.view.log_viewer.log_viewer_widget import LogViewerWidget
from utils.logger import get_logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MVC Image Processor")
        self.resize(1000, 700)

        self.setStyleSheet(f"""
            #MainWindow {{
                background-color: {Theme.background_color};
            }}
            QPushButton {{
                background-color: {Theme.primary_color};
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{
                background-color: #005f99;
            }}
        """)
        get_logger().info("MainWindow initialized.")
        # Main background color
        self.setObjectName("MainWindow")

        # Column first : App bar and main panel
        self.appbar = QWidget()
        self.appbar.setFixedHeight(50)
        self.appbar.setStyleSheet(f"background-color: {Theme.primary_dark};")

        layout = QVBoxLayout()
        layout.addWidget(self.appbar)

        # Main Panel layout : Side panel on left, image viewer and log on right (vertically)

        self.side_panel = QWidget()
        self.side_panel.setFixedWidth(200)
        self.side_panel.setStyleSheet(f"background-color: {Theme.overlay_background_color};")
        self.Image_viewer = QWidget()
        self.Image_viewer.setStyleSheet(f"background-color: {Theme.overlay_background_color};")
        self.Image_viewer.setMinimumHeight(400) 
        self.log_viewer = LogViewerWidget()

        self.main_panel_layout = QHBoxLayout()
        self.main_panel_layout.addWidget(self.side_panel)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.Image_viewer, stretch=3)
        right_layout.addWidget(self.log_viewer, stretch=1)
        self.main_panel_layout.addLayout(right_layout)
        self.main_panel = QWidget()
        self.main_panel.setLayout(self.main_panel_layout)
        layout.addWidget(self.main_panel)

        # self.side_panel = SidePanel()
        # self.viewer = ImageSection()

        # layout = QHBoxLayout()
        # layout.addWidget(self.side_panel)
        # layout.addWidget(self.viewer)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
