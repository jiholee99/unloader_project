from core.image_grab import ImageGrabService
from adapters.image_grab import CameraGrabber

from exceptions.exception import FactoryException

from utils.logger import get_logger

logger = get_logger("Grabber Factory")

class CameraGrabberFactory:
    @staticmethod
    def create():
        try:
            logger.info("Creating Camera Grabber Service...")
            windows_camera = CameraGrabber()
            image_grab_service = ImageGrabService(grabber=windows_camera)
            logger.info("Camera Grabber Service created successfully.")
            return image_grab_service
        except Exception as e:
            raise FactoryException("Failed to create Camera Grabber Service.", e)
        