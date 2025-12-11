import numpy as np
from exceptions.exception import ImageGrabException
from core.interfaces import Grabber
from utils.logger import get_logger


class PiCameraGrabber(Grabber):
    def __init__(self, config: dict = {}):
        self.config = config
        self.logger = get_logger("PiCameraGrabber")
        self.camera = None

    def __del__(self):
        self.logger.warning(
            "Releasing PiCamera resources. This should happen only when the app is terminating."
        )
        self.close()

    def init_grabber(self):
        """Initialize the PiCamera once."""
        try:
            from picamera2 import Picamera2
            self.camera = Picamera2()

            # Load configuration (resolution, format, etc.)
            preview_config = self.camera.create_preview_configuration(
                main={
                    "size": self.config.get("resolution", (640, 480)),
                    "format": "RGB888"
                }
            )
            self.camera.configure(preview_config)
            self.camera.start()

            self.logger.info("PiCamera initialized successfully.")

        except Exception as e:
            raise ImageGrabException(f"Failed to initialize PiCamera: {e}")

    def grab_image(self, timeout=1.0):
        if self.camera is None:
            raise ImageGrabException("PiCamera not initialized. Call init_grabber() first.")
        print("Grabbing Image")
        import time
        start = time.time()

        while True:
            req = self.camera.capture_request(wait=False)

            if req is not None:
                # Extract image properly
                frame = req.get_result(timeout=5).make_array("main")
                print("Grab done")
                return frame

            if time.time() - start > timeout:
                raise ImageGrabException("Camera capture timed out – sensor stalled.")
        
            time.sleep(0.01)



    def close(self):
        """Release the camera gracefully."""
        if self.camera is not None:
            try:
                self.camera.stop()
            except Exception:
                pass  # Sometimes stop() throws harmless errors

            self.camera.close()
            self.camera = None
            self.logger.info("PiCamera released.")
