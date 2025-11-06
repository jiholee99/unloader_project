import cv2
from PySide6.QtWidgets import QFileDialog
from ui.model.image_model import ImageModel
from ui.view.main_window import MainWindow
# Viewers
from ui.view.options_viewer.options_viewer_widget import OptionsViewer
from ui.view.image_viewer.image_viewer_widget import ImageViewerWidget
# Controllers
from ui.controller.options_controller import OptionsController
from ui.controller.image_controller import ImageController
class MainController:
    def __init__(self, main_window):
        self.main_window = main_window

        # Shared models
        self.image_model = ImageModel()
        
        # Controllers
        self.options_controller = OptionsController(image_model=self.image_model, view=self.main_window.options_viewer)
        self.image_controller = ImageController(model=self.image_model, view=self.main_window.image_viewer)

        self.options_controller.image_requested.connect(self.image_controller.load_and_update)

        self.options_controller.image_requested.connect(self.image_controller.load_and_update)

