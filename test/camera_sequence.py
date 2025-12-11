# Factories
from app.factories import InspectionFactory
# Adapters
from adapters.config import AppConfigAdapter
from adapters.image_process import ImagePreprocessor
from adapters.remote_capture import DirectConnector, UrlRequestor
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
import os
import shutil
import uuid
import cv2

class CameraSequence:
    def __init__(self, inspection_service: InspectionService, grabber_service: ImageGrabService):
        self.logger = get_logger("Test Sequence")
        self.inspection_service = inspection_service
        self.grabber_service = grabber_service


    def cleanup_storage(self,directory, threshold=80):
        """Delete oldest files until usage is below the threshold."""
        usage = shutil.disk_usage(directory)
        percent_used = usage.used / usage.total * 100
        
        if percent_used < threshold:
            return  # nothing to clean
        
        # List all files sorted by oldest first
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
        files.sort(key=lambda x: os.path.getmtime(x))  # sort by modification time

        # Keep deleting oldest files until under threshold
        for file in files:
            print(f"Deleting {file}")
            os.remove(file)

            usage = shutil.disk_usage(directory)
            percent_used = usage.used / usage.total * 100

            if percent_used < threshold:
                break

    def save_image_with_fifo(self,image_bytes, directory, filename, threshold=80):
        os.makedirs(directory, exist_ok=True)

        # Step 1 → cleanup if needed
        self.cleanup_storage(directory, threshold)

        # Step 2 → save image
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        print(f"Saved: {filepath}")



    def _grab_image(self) -> np.ndarray:
        self.logger.info("Grabbing image...")
        image = self.grabber_service.grab_image()
        self._save_image(image=image)
        self.logger.info("Grabbed image successfully.")
        return image
    
    def _run_inspection(self, image):
        return
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
    


    def _save_image_random(self,image : np.ndarray, directory, ext="jpeg"):
        
        os.makedirs(directory, exist_ok=True)

        self.cleanup_storage(directory)

        # Convert RGB → BGR if needed
        if image.shape[-1] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Generate random filename
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(directory, filename)

        if not cv2.imwrite(filepath, image):
            raise Exception(f"Failed to save image to {filepath}")

        return filepath


    def _remote_capture(self):
        return
        # return
        app_state.controller.update_result(text="Simulating remote image capture...") if app_state.controller else None
        try:
            config = AppConfigAdapter().load_remote_camera_options()
            url_requestor = UrlRequestor(config=config)
            remote_capture_service = RemoteCaptureService(remote_capture_repository=url_requestor)
            remote_capture_service.remote_capture()
        except Exception as e:
            app_state.controller.update_result(text="Remote capture failed.") if app_state.controller else None
            raise SequenceException("Remote capture failed during sequence execution.", e)
        finally:
            app_state.controller.update_result(text="Remote image capture simulation completed.") if app_state.controller else None
        
        return
        
    def _attach_bobbin_info(self):
        return
        app_state.controller.update_result(text="Simulating bobbin info attachment...") if app_state.controller else None
        time.sleep(1)  # Simulate delay
        app_state.controller.update_result(text="Bobbin info attachment simulation completed.") if app_state.controller else None
        return
        # raise NotImplementedError("Bobbin info attachment not implemented yet.")

    def _upload_results(self):
        return
        app_state.controller.update_result(text="Simulating result upload...") if app_state.controller else None
        try:
            config = AppConfigAdapter().load_image_uploader_options()
            minpc_uploader = MiniPCUploader(config=config)
            uploader_service = ImageUploaderService(uploader_repository=minpc_uploader, config=config)
            uploader_service.upload(dest_path="/Unloader2")
        except Exception as e:
            app_state.controller.update_result(text="Result upload failed.") if app_state.controller else None
            raise SequenceException("Result upload failed during sequence execution.", e)
        app_state.controller.update_result(text="Result upload simulation completed.") if app_state.controller else None
        return


    def run(self):
        try:
            # Grab Image
            grabbed_image = self._grab_image()

            # Inspection Service Setup
            self.logger.info("Starting inspection simulation...")
            self._run_inspection(grabbed_image)
            if app_state.controller:
                app_state.controller.update_panel(0, title="Test Sequence", image=grabbed_image)
                app_state.controller.update_result(text="Inspection completed successfully.")
                pass
            self.logger.info("Inspection simulation completed.")

            self._save_image(grabbed_image)
            self._save_image_random(grabbed_image, directory="/media/lgvision/1622-6885/unloader_images")

            # Send signal to two other pi to grab images
            self.logger.info("Starting remote capture simulation...")
            self._remote_capture()
            self.logger.info("Remote capture simulation completed.")
             
            # Retrieve bobbin info from database and attach to result
            self._attach_bobbin_info()

            # Upload results to database
            self.logger.info("Starting result upload simulation...")
            self._upload_results()
            self.logger.info("Result upload simulation completed.")

        except Exception as e:
            if app_state.controller:
                error_text = f"Sequence Error occurred during sequence execution ->  {str(e)}"
                app_state.controller.update_result(text=error_text)
            raise SequenceException("Sequence Error occurred during sequence execution.", e)