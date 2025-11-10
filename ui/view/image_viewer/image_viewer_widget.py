from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from ui.view.default_widgets.default_viewer_container_widget import DefaultViewerContainerWidget
from ui.view.default_widgets.default_image_display import DefaultImageDisplay
from ui.model.image_model import ImageModel
class ImageViewerWidget(QWidget):
    def __init__(self, parent=None, model : ImageModel = None):
        super().__init__(parent)
        self.model = model if model is not None else ImageModel()

        # Example inner content widget
        self.preprocssed_display = DefaultImageDisplay(title="Live Edit Image")
        self.original_display = DefaultImageDisplay(title="Result Image")
        self.image_display = QWidget()
        image_layout = QHBoxLayout(self.image_display)
        image_layout.setContentsMargins(5, 5, 5, 5)
        image_layout.setSpacing(10)
        image_layout.addWidget(self.preprocssed_display)
        image_layout.addWidget(self.original_display)

        

        # Wrap it inside the reusable container
        container = DefaultViewerContainerWidget(
            title="Image Viewer",
            child_widget=self.image_display
        )

        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)
        self.setMinimumHeight(450)
        self.setMinimumWidth(900)
