# controller/options_controller.py
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog
from ui.model.image_model import ImageModel

class OptionsController(QObject):
    def __init__(self, view, model : ImageModel = None, image_view = None):
        super().__init__()
        self.view = view
        self.model = model if model is not None else ImageModel()
        self.image_view = image_view
        self.setup_connections()

    def setup_connections(self):
        # Connect child view signals to controller handlers
        self.view.settings_scrollview.child_widget.button1_clicked.connect(self.handle_option1_clicked)
        self.view.button.clicked.connect(self.handle_main_button)
    
    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None,  # Parent widget, None means no parent
            "Select a File",  # Dialog title
            "",  # Starting directory, empty means default
            "All Files (*.*)"  # File filter
        )
        return file_path

    def handle_option1_clicked(self):
        print("Option 1 clicked in child view")
        # Show file dialog or perform some action
        path = self.select_file()
        if path:
            # self.model.load_image(path)
            if self.image_view:
                self.image_view.model.load_image(path)
                self.image_view.preprocssed_display.update_image_view()
        
        # self.view.option1_applied.emit()  # re-emit to higher layers if needed

    def handle_main_button(self):
        print("Main 'Click Me' button clicked")
