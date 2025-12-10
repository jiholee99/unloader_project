# Factories
from app.factories import InspectionFactory
# Adapters
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
# Core Services
from core.image_grab import ImageGrabService
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService
from core.remote_capture import RemoteCaptureService
from core.uploader import ImageUploaderService

# Exceptions
from exceptions.exception import SequenceException

# Utils
import numpy as np
from utils.logger import get_logger

# UI State
from core import app_state


class Sequence:
    def __init__(self, inspection_service: InspectionService, grabber_service: ImageGrabService):
        self.logger = get_logger("Sequence")
        self.inspection_service = inspection_service
        self.grabber_service = grabber_service

    def _save_image(self, image: np.ndarray, path: str = "assets/test_images/grabbed_image.jpeg") -> None:
        import cv2
        cv2.imwrite(path, image)

    def _grab_image(self) -> np.ndarray:
        self.logger.info("Grabbing image...")
        image = self.grabber_service.grab_image()
        # self._save_image(image=image)
        self.logger.info("Grabbed image successfully.")
        return image
    
    def _run_inspection(self, image):
        try:
            self.logger.info("Initiating inspection service...")
            self.inspection_service.inspect(image)
            self.inspection_service.debug_save_image(image=image)
            self.logger.info("Inspection service completed.")
        except Exception as e:
            raise SequenceException("Inspection service failed during sequence execution.", e)

    def _grab_all_images(self):
        return
        # Pseudo code for grabbing images from remote devices
        # remote_capture_service = RemoteCaptureService("repo")
        # remote_capture_service.capture_all()

    def _attach_bobbin_info(self):
        return
        # raise NotImplementedError("Bobbin info attachment not implemented yet.")

    def _upload_results(self):
        return
        # Pseudo code for uploading results
        # uploader = ImageUploaderService("repo")
        # uploader.upload("file_path")
        # raise NotImplementedError("Result upload not implemented yet.")

    def run(self):
        try:
            # Grab Image
            grabbed_image = self._grab_image()

            # Inspection Service Setup
            self._run_inspection(grabbed_image)
            if app_state.controller:
                # app_state.controller.update_result(text="Inspection completed successfully.")
                pass

            # Send signal to two other pi to grab images
            self._grab_all_images()
             
            # Retrieve bobbin info from database and attach to result
            self._attach_bobbin_info()

            # Upload results to database
            self._upload_results()

        except Exception as e:
            if app_state.controller:
                error_text = f"Sequence Error occurred during sequence execution ->  {str(e)}"
                app_state.controller.update_result(text=error_text)
            raise SequenceException("Sequence Error occurred during sequence execution.", e)