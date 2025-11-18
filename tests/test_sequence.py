# Factories
from app.factory import InspectionFactory
# Adapters
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
from adapters.image_grab import CameraGrabber, FileGrabber
# Core Services
from core.image_grab import ImageGrabService
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService

# Exceptions
from exceptions.exception import SequenceException

# Utils
import numpy as np
from utils.logger import get_logger


class TestSequence:
    def __init__(self):
        self.logger = get_logger("Test Sequence")

    def _grab_image(self) -> np.ndarray:
        grabber = CameraGrabber()
        image_grab_service = ImageGrabService(grabber=grabber)
        image = image_grab_service.grab_image()
        return image
    
    def _run_inspection(self, image):
        inspection_service = InspectionFactory.create()
        inspection_service.inspect(image)

    def _grab_all_images(self):
        raise NotImplementedError("Multi-image grabbing not implemented yet.")

    def _attach_bobbin_info(self):
        raise NotImplementedError("Bobbin info attachment not implemented yet.")

    def _upload_results(self):
        raise NotImplementedError("Result upload not implemented yet.")

    def run(self):
        try:
            self.logger.info("Grabbing image...")
            grabbed_image = self._grab_image()
            self.logger.info("Grabbed image successfully.")

            # Inspection Service Setup
            config = AppConfigAdapter()
            self._run_inspection(grabbed_image)

            # Send signal to two other pi to grab images
            self._grab_all_images()
             
            # Retrieve bobbin info from database and attach to result
            self._attach_bobbin_info()

            # Upload results to database
            self._upload_results()

        except Exception as e:
            raise SequenceException("Error occurred during sequence execution.", e)