from core.image_grab.image_grab_service import ImageGrabService
from core.inspection.inspection_service import InspectionService
from exceptions.exception import AppException
import numpy as np
from utils.logger import get_logger
class Sequence:
    def __init__(self):
        self.logger = get_logger()

    def _grab_image(self) -> np.ndarray:
        return ImageGrabService().grab_image_from_camera()
        return ImageGrabService().grab_image_from_file(image_path=r"assets\test_images\full.jpeg")

    def _run_inspection(self, image):
        inspection_service = InspectionService()
        inspection_service.inspect(image)

    def _grab_all_images(self):
        pass

    def _attach_bobbin_info(self):
        pass

    def _upload_results(self):
        pass

    def run(self):
        try:
            self.logger.info("Grabbing image...")
            grabbed_image = self._grab_image()
            self.logger.info("Grabbed image successfully.")

            self._run_inspection(grabbed_image)
            self._grab_all_images()
            self._attach_bobbin_info()
            self._upload_results()
        except AppException as ae:
            self.logger.error(f"Application error during sequence run: {ae}")
        except Exception as e:
            self.logger.error(f"Sequence run failed: {e}")
