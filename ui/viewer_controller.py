# viewer/viewer_controller.py

from PySide6.QtCore import QObject, Signal


class ViewerController(QObject):
    """
    Controller:
    - updates model
    - emits signals to view
    """

    sig_update_title = Signal(int, str)
    sig_update_image = Signal(int, object)
    sig_update_result = Signal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.runner_thread = None


        # connect controller signals to view slots
        self.sig_update_title.connect(view.update_title)
        self.sig_update_image.connect(view.update_image)
        self.sig_update_result.connect(view.update_result)
    
    def set_runner_thread(self, thread):
        self.runner_thread = thread

    # ================================================================
    # PUBLIC API CALLS (used by your app)
    # ================================================================
    def update_panel(self, index, title=None, image=None):
        if title is not None:
            self.model.panel_titles[index] = title
            self.sig_update_title.emit(index, title)

        if image is not None:
            self.model.panel_images[index] = image
            self.sig_update_image.emit(index, image)

    def update_result(self, text):
        self.model.result_text = text
        self.sig_update_result.emit(text)
