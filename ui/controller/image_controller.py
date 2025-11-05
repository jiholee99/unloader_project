from PySide6.QtWidgets import QWidget, QFileDialog
from ui.model.image_model import ImageModel

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.setup_connections()

    def setup_connections(self):
        self.view.load_button.clicked.connect(self.select_image)

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
