# viewer/viewer_model.py

class ViewerModel:
    """
    Stores titles and images for 4 fixed panels + result text.
    """

    def __init__(self):
        self.panel_titles = ["original", "croped", "processed", "overlay"]
        self.panel_images = [None, None, None, None]
        self.result_text = ""
