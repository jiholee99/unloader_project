import cv2
from PySide6.QtWidgets import QFileDialog
from ui.model.image_model import ImageModel
from ui.view.main_window import MainWindow

class MainController:
    def __init__(self):
        self.model = ImageModel()
        self.view = MainWindow()

        # connect signals
        # self.view.side_panel.load_image_clicked.connect(self.load_image)
        # self.view.side_panel.process_clicked.connect(self.process_image)
        # self.view.side_panel.quit_clicked.connect(self.view.close)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self.view, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        img = self.model.load_image(path)
        self.view.viewer.show_image(img)

    def process_image(self):
        processed = self.model.apply_threshold(threshold=150)
        self.view.viewer.show_image(processed)

    def show(self):
        self.view.show()
