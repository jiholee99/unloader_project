from typing import List
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider, QSizePolicy, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from ui.view.default_widgets.default_button import DefaultButton

class Options(QWidget):
    load_image_clicked = Signal()
    user_changed_option = Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        # load_image_button = DefaultButton("Load Image")
        # layout.addWidget(load_image_button)

        # Image options section
        # Will define buttons and add it to the options container
        image_options_buttons = []
        load_image_button = DefaultButton("Load Image")
        set_roi_button = DefaultButton("Set ROI")
        show_original_button = DefaultButton("Show Original")
        image_options_buttons.append(load_image_button)
        image_options_buttons.append(set_roi_button)
        image_options_buttons.append(show_original_button)
        options_container = OptionsContainer(children=image_options_buttons, title_text="Image Options")

        layout.addWidget(options_container)

        # Preprocess options section
        preprocess_options_buttons = []
        self.threshold_label = QLabel("Threshold: 128")
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(128)
        self.threshold_slider.valueChanged.connect(self._on_slider_change)
        preprocess_options_buttons.append(self.threshold_label)
        preprocess_options_buttons.append(self.threshold_slider)
        # Add preprocess option buttons here
        preprocess_options_container = OptionsContainer(children=preprocess_options_buttons, title_text="Preprocess Options")



        layout.addWidget(preprocess_options_container)


        # Postprocess options section
        postprocess_options_buttons = []
        use_fill_holes_checkbox = DefaultButton("Fill Holes")
        detect_contours_button = DefaultButton("Detect Contours")
        checkbox = QCheckBox("Sample Checkbox")
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: white;
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 6px;
                background-color: {Theme.overlay_background_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Theme.primary_color};
            }}
            """)
        postprocess_options_buttons.append(use_fill_holes_checkbox)
        postprocess_options_buttons.append(detect_contours_button)
        postprocess_options_buttons.append(checkbox)
        # Add postprocess option buttons here
        postprocess_options_container = OptionsContainer(children=postprocess_options_buttons, title_text="Postprocess Options")
        layout.addWidget(postprocess_options_container)

        # Sample section: Threshold slider
        sample_options_container = OptionsContainer(title_text="Sample Option")
        layout.addWidget(sample_options_container)



        
        # layout.addWidget(self.threshold_label)
        # layout.addWidget(self.threshold_slider)

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



class OptionsContainer(QWidget):
    def __init__(self, parent=None, children: List[QWidget] = None, title_text="Options"):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel(title_text)
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 2px 4px;
        """)
        title.setAlignment(Qt.AlignLeft)

        layout.addWidget(title, stretch=0)  # title minimal height

        children_layout = QVBoxLayout()
        if children:
            for child in children:
                children_layout.addWidget(child)
        children_layout.setAlignment(Qt.AlignTop)
        layout.addLayout(children_layout, stretch=1)  # main content expands

        divider = QWidget()
        divider.setFixedHeight(2)
        divider.setStyleSheet("background-color: white;")
        layout.addWidget(divider, stretch=0)  # divider minimal height
        divider.setContentsMargins(0,0,0,10)

        self.setLayout(layout)


from ..config.theme import Theme
from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt

class DefaultCheckBox(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setObjectName("DefaultCheckBox")
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)
        
        # Create label
        self.label = QLabel(text)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 14px;
            }}
        """)
        
        # Create checkbox - using native style
        self.checkbox = QCheckBox()
        
        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.checkbox)
        
        # Style the container
        self.setStyleSheet(f"""
            #DefaultCheckBox {{
                background-color: red;
                border: none;
                border-radius: 6px;
            }}
            #DefaultCheckBox:hover {{
                background-color: #005f99;
            }}
            QCheckBox::pressed
            {{
            background-color : lightgreen;
            }}
            QCheckBox::checked
            {{
            background-color : lightgreen;
            }}
        """)
    
    def isChecked(self):
        return self.checkbox.isChecked()
    
    def setChecked(self, checked):
        self.checkbox.setChecked(checked)
    
    def setText(self, text):
        self.label.setText(text)