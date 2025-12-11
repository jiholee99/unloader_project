# viewer/viewer_view.py

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGridLayout, QSizePolicy, QTextEdit, QHBoxLayout,
)
from PySide6.QtCore import Qt, Slot
from utils.image_renderer import ImageRenderer
from PySide6.QtGui import QTextCursor

class ViewerView(QWidget):
    """
    UI Layout:
    - 4 image panels (2x2 grid)
    - Large text result section at bottom
    """

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("MVC Multi Panel Viewer")
        self.resize(1400, 600)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # ---- 2x2 grid for four panels ----
        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)
        self.main_layout.setStretchFactor(self.grid, 3)

        self.title_labels = []
        self.image_labels = []

        for i in range(4):
            panel_widget = self._create_panel(i)
            r = i // 2
            c = i % 2
            self.grid.addWidget(panel_widget, r, c)

        # ---- Result section at bottom ----
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumHeight(150)
        self.result_box.setStyleSheet("font-size: 12px; padding: 10px;")
        self.main_layout.addWidget(self.result_box)

    def closeEvent(self, event):
        from core import app_state
        controller = app_state.controller

        if controller and controller.runner_thread:
            controller.runner_thread.request_stop()
            controller.runner_thread.wait()  # block until thread exits

        event.accept()
        
    def _create_panel(self, index):
        title = QLabel(self.model.panel_titles[index])
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background: #333; color: white; padding: 6px;")

        image_label = QLabel("No Image")
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label.setMinimumSize(400, 300)
        image_label.setStyleSheet("background: #111; color: #777; padding: 10px;")

        container = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(container)

        container.addWidget(title)
        container.addWidget(image_label)

        self.title_labels.append(title)
        self.image_labels.append(image_label)

        return widget

    # =====================================================================
    # PUBLIC UI UPDATE FUNCTIONS (Used by Controller)
    # =====================================================================

    @Slot(int, str)
    def update_title(self, index, title_text):
        self.title_labels[index].setText(title_text)

    @Slot(int, object)
    def update_image(self, index, cv_img):
        if cv_img is None:
            return

        qimg = ImageRenderer.cv_to_qimage(cv_img)
        if qimg is None:
            return

        label = self.image_labels[index]
        pix = ImageRenderer.scale_for_label(qimg, label)
        if pix:
            label.setPixmap(pix)

    @Slot(str)
    def update_result(self, result_text):
        import time
        self.result_box.append(f"At [{time.strftime('%H:%M:%S')}] ")
        self.result_box.append(f"- {result_text}\n\n")
        self.result_box.moveCursor(QTextCursor.End)
