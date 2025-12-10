# Factories
from app.factories import InspectionFactory
# Adapters
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
from adapters.remote_capture import DirectConnector
from adapters.image_uploader import MiniPCUploader
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

import time

class TestSequence:
    def __init__(self, inspection_service: InspectionService, grabber_service: ImageGrabService):
        self.logger = get_logger("Test Sequence")
        self.inspection_service = inspection_service
        self.grabber_service = grabber_service

    def _grab_image(self) -> np.ndarray:
        self.logger.info("Grabbing image...")
        image = self.grabber_service.grab_image()
        # self._save_image(image=image)
        self.logger.info("Grabbed image successfully.")
        return image
    
    def _run_inspection(self, image):
        try:
            # Mock inspection by just returning True
            time.sleep(3)
            return True
        except Exception as e:
            raise SequenceException("Inspection service failed during sequence execution.", e)

    def _save_image(self, image: np.ndarray):
        if app_state.controller:
            app_state.controller.update_result(text="Saving inspection result image...")
        import cv2
        cv2.imwrite("assets/saved_images/inspection_result.jpeg", image)
        if app_state.controller:
            app_state.controller.update_result(text="Inspection result image saved successfully.")

    def _remote_capture(self):
        return
        app_state.controller.update_result(text="Simulating remote image capture...") if app_state.controller else None
        config = AppConfigAdapter().load_remote_camera_options()
        dirct_connector = DirectConnector(config=config)
        remote_capture_service = RemoteCaptureService(remote_capture_repository=dirct_connector)
        remote_capture_service.remote_capture()
        app_state.controller.update_result(text="Remote image capture simulation completed.") if app_state.controller else None
        return
        # Pseudo code for grabbing images from remote devices
        # remote_capture_service = RemoteCaptureService("repo")
        # remote_capture_service.capture_all()

    def _attach_bobbin_info(self):
        app_state.controller.update_result(text="Simulating bobbin info attachment...") if app_state.controller else None
        time.sleep(1)  # Simulate delay
        app_state.controller.update_result(text="Bobbin info attachment simulation completed.") if app_state.controller else None
        return
        # raise NotImplementedError("Bobbin info attachment not implemented yet.")

    def _upload_results(self):
        app_state.controller.update_result(text="Simulating result upload...") if app_state.controller else None
        minpc_uploader = MiniPCUploader()
        uploader_service = ImageUploaderService(uploader_repository=minpc_uploader)
        uploader_service.upload(dest_path="/Samples", file_path="/home/lgvision/projects/new/unloader_project/assets/saved_images/inspection_result.jpeg")
        app_state.controller.update_result(text="Result upload simulation completed.") if app_state.controller else None
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
                app_state.controller.update_panel(0, title="Test Sequence", image=grabbed_image)
                app_state.controller.update_result(text="Inspection completed successfully.")
                pass

            self._save_image(grabbed_image)

            # Send signal to two other pi to grab images
            self._remote_capture()
             
            # Retrieve bobbin info from database and attach to result
            self._attach_bobbin_info()

            # Upload results to database
            self._upload_results()

        except Exception as e:
            if app_state.controller:
                error_text = f"Sequence Error occurred during sequence execution ->  {str(e)}"
                app_state.controller.update_result(text=error_text)
            raise SequenceException("Sequence Error occurred during sequence execution.", e)