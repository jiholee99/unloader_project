# Factories
from app.factories import InspectionFactory
# Adapters
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
# Core Services
from core.image_grab import ImageGrabService
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService

# Exceptions
from exceptions.exception import SequenceException
from ui.debug_view import DebugImageViewer
# Utils
import numpy as np
from utils.logger import get_logger


class TestSequence:
    def __init__(self, inspection_service: InspectionService, grabber_service: ImageGrabService):
        self.logger = get_logger("Test Sequence")
        self.inspection_service = inspection_service
        self.grabber_service = grabber_service

    def _grab_image(self) -> np.ndarray:
        image = self.grabber_service.grab_image()
        return image
    
    def _run_inspection(self, image):
        self.inspection_service.inspect(image)
        self.inspection_service.debug_save_image(image=image)

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
            self._run_inspection(grabbed_image)

            # Send signal to two other pi to grab images
            self._grab_all_images()
             
            # Retrieve bobbin info from database and attach to result
            self._attach_bobbin_info()

            # Upload results to database
            self._upload_results()

        except Exception as e:
            raise SequenceException("Sequence Error occurred during sequence execution.", e)