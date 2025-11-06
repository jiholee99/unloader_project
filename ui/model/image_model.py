import cv2
import numpy as np

from core.process.pre_process.image_pre_process_service import ImagePreprocessService
from core.process.post_process.image_post_processor_service import ImagePostProcessorService
from main import get_roi_coordinates
from utils.app_config_handler import AppConfigHandler

class ImageModel:
    """Handles all image data and OpenCV processing logic."""

    def __init__(self):
        self.image = None
        self.processed_image = None

    def load_image(self, path: str):
        self.image = cv2.imread(path)
        if self.image is None:
            raise FileNotFoundError("Could not load image.")
        return self.image

    def load_processed_image(self, path: str):
        image = cv2.imread(path)
        service = ImagePreprocessService(options=AppConfigHandler.get_preprocess_options())
        preprocessor_config = AppConfigHandler.get_preprocess_options()
        x, y, w, h = get_roi_coordinates()
        roi_coords = [x, y, w, h]
        threshold_value = preprocessor_config.get("threshold", 10)
        processed_mask = service.process_image(image=image, roi_coords=roi_coords, threshold=threshold_value)
        post_process_service = ImagePostProcessorService(options=AppConfigHandler.get_postprocess_options())
        processed_mask = post_process_service.post_process(processed_mask)
        return processed_mask

    def load_cv2_image(self, path: str):
        self.image = cv2.imread(path)
        if self.image is None:
            raise FileNotFoundError("Could not load image.")
        cv_img = np.ascontiguousarray(self.image, dtype=np.uint8)
        cv_img = cv_img.copy(order='C')  # ensures aligned memory layout
        return cv_img

    def apply_threshold(self, threshold=128):
        if self.image is None:
            raise ValueError("No image loaded.")
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        self.processed_image = mask
        return self.processed_image
