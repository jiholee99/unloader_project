import sys
from PySide6.QtWidgets import QApplication
from ui.controller.main_controller import MainController
from ui.controller.options_controller import OptionsController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    options_controller = OptionsController(view=controller.view.options_viewer, image_view=controller.view.image_viewer)
    controller.show()
    sys.exit(app.exec())
