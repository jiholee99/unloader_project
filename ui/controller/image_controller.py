from PySide6.QtWidgets import QWidget, QFileDialog
from ui.model.image_model import ImageModel
from ui.view.image_viewer.image_viewer_widget import ImageViewerWidget
import numpy as np
class ImageController:
    def __init__(self, model : ImageModel, view: ImageViewerWidget):
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        # self.view.load_button.clicked.connect(self.select_image)
        pass

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.model.image = file_path
            self.view.update_image_view()  # 👈 manually refresh
    
    def load_and_update(self, image_path):
        # self.model.load_image(image_path)
        preprocessed_img = self.model.load_processed_image(image_path)
        original_img = self.model.load_cv2_image(image_path)
        self.view.preprocssed_display.update_image_view(cv_img=preprocessed_img)  # 👈 manually refresh
        self.view.original_display.update_image_view(cv_img=original_img)  # 👈 manually refresh