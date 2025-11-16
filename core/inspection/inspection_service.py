import cv2
from exceptions.exception import InspectionException
from core.image_grab.image_grab_service import ImageGrabService
from core.inspection.process.pre_process.image_pre_process_service import ImagePreprocessService
from core.inspection.process.post_process.image_post_processor_service import ImagePostProcessorService
from utils.visual_debugger import show_scaled
import numpy as np
from utils.app_config_handler import AppConfigHandler
from utils.logger import get_logger

class InspectionService:
    def __init__(self):
        self.pre_processed_image = None
        self.post_processed_image = None
        self.pre_process_options = {}
        self.post_process_options = {}
        self.judgement_options = {}
        self.roi_coords = []
        self.logger = get_logger()

    def _load_config(self):
        self.pre_process_options = AppConfigHandler.get_preprocess_options()
        self.post_process_options = AppConfigHandler.get_postprocess_options()
        self.judgement_options = AppConfigHandler.get_judgement_options()
        roi = AppConfigHandler.get_roi_settings()
        self.roi_coords = [roi["x"], roi["y"], roi["w"], roi["h"]]

    def _pre_process_image(self, image: np.ndarray) -> np.ndarray:
        self.logger.info("Starting image preprocessing...")
        pre_process_service = ImagePreprocessService(options=self.pre_process_options)
        processed_mask = pre_process_service.process_image(image=image, roi_coords=self.roi_coords)
        show_scaled(f"Processed Mask", processed_mask)
        self.logger.info("Image preprocessing completed.")
        return processed_mask

    def _post_process_image(self, pre_processed_image: np.ndarray) -> np.ndarray:
        self.logger.info("Starting image postprocessing...")
        post_process_service = ImagePostProcessorService(options=self.post_process_options)
        processed_image = post_process_service.post_process(mask=pre_processed_image)
        show_scaled(f"Post Processed Image", processed_image)
        self.logger.info("Image postprocessing completed.")
        return processed_image

    def _is_roller(self):
        pass

    def _is_close(self):
        pass

    def inspect(self, image : np.ndarray):
        try:
            self._load_config()
            pre_processed_image = self._pre_process_image(image=image)
            post_processed_image = self._post_process_image(pre_processed_image=pre_processed_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            roller_status = self._is_roller()
            close_status = self._is_close()
        except Exception as e:
            raise InspectionException("Inspection process error occurred.", e)
        

        pass


if __name__ == "__main__":
    service = InspectionService()
    service.inspect()