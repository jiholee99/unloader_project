from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from ui.view.default_widgets.default_button import DefaultButton

class Options(QWidget):
    load_image_clicked = Signal()
    user_changed_option = Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        load_image_button = DefaultButton("Load Image")
        layout.addWidget(load_image_button)

        self.threshold_label = QLabel("Threshold: 128")
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(128)
        self.threshold_slider.valueChanged.connect(self._on_slider_change)
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.threshold_slider)

        load_image_button.clicked.connect(self.load_image_clicked.emit)
    
    def show_options(self, options: dict):
        """Called by controller when options change."""
        self.threshold_slider.setValue(options.get("threshold", 128))
        # self.threshold_label.setText(f"Threshold: {options.get('threshold', 128)}")
        # self.auto_save_checkbox.setChecked(options.get("auto_save", False))

    def _on_slider_change(self, value):
        self.threshold_label.setText(f"Threshold: {value}")
        # self.user_changed_option.emit("threshold", value)

    def _on_checkbox_change(self, state):
        self.user_changed_option.emit("auto_save", bool(state))