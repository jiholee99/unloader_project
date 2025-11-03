from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from ui.view.default_widgets.default_title_container_widget import DefaultContainerTitleWidget
from ui.view.default_widgets.default_scrollview import DefaultScrollView
from ui.view.default_widgets.default_button import DefaultButton
from ui.view.config.theme import Theme

class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        outer = QWidget()

        outer.setContentsMargins(5, 5, 5, 5)
        outer.setObjectName("SidePanel")
        outer.setStyleSheet(f"""
            #SidePanel {{
                background-color: {Theme.overlay_background_color};
                border-radius: 15px;
            }}
        """)

        # Outer layer is the container with rounded corners. title and log display here
        outer_layout = QVBoxLayout(outer)

        self.title_fullview_widget = DefaultContainerTitleWidget(title="Side Panel")
        outer_layout.addWidget(self.title_fullview_widget)

        placeholder_text = "sddasd\n" * 50  # Placeholder text
        text = QLabel(placeholder_text)
        self.settings_scrollview = DefaultScrollView(child_widget=text)
        outer_layout.addWidget(self.settings_scrollview, stretch=1)

        self.button = DefaultButton("Click Me")
        outer_layout.addWidget(self.button)

        # Now make 'outer' the only thing inside self.layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(outer)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(400)
        self.setMinimumWidth(350) 



