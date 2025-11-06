import sys
from PySide6.QtWidgets import QApplication
from ui.view.main_window import MainWindow
from ui.controller.main_controller import MainController
from ui.controller.options_controller import OptionsController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    controller = MainController(main_window=main_window)
    main_window.show()
    sys.exit(app.exec())
