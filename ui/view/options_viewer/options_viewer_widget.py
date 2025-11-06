from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal
from ui.view.default_widgets.default_title_container_widget import DefaultContainerTitleWidget
from ui.view.default_widgets.default_scrollview import DefaultScrollView
from ui.view.default_widgets.default_button import DefaultButton
from ui.view.config.theme import Theme
from ui.view.default_widgets.default_viewer_container_widget import DefaultViewerContainerWidget

from ui.view.options_viewer.options import Options
from ui.model.image_model import ImageModel

class OptionsViewer(QWidget):    
    def __init__(self, parent=None, model :ImageModel = None):
        super().__init__(parent)
        self.model = model
    
        placeholder_text = "sddasd\n" * 50  # Placeholder text
        options = Options()
        self.settings_scrollview = DefaultScrollView(child_widget=options)

        self.button = DefaultButton("Apply Options")

        # Child to pass in to DefaultViewerContainerWidget
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)
        outer_layout.addWidget(self.settings_scrollview, stretch=1)
        outer_layout.addWidget(self.button, stretch=0)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Wrap it inside the reusable container
        container = DefaultViewerContainerWidget(
            title="Options",
            child_widget=outer
        )

        # Now make 'container' the only thing inside self.layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumHeight(400)
        self.setMinimumWidth(350) 



