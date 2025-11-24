from core.image_grab import ImageGrabService
from adapters.image_grab import PiCameraGrabber

from exceptions.exception import FactoryException

from utils.logger import get_logger

logger = get_logger("Grabber Factory")

class PiCameraGrabberFactory:
    @staticmethod
    def create():
        try:
            logger.info("Creating Pi Camera Grabber Service...")
            pi_camera = PiCameraGrabber()
            image_grab_service = ImageGrabService(grabber=pi_camera)
            logger.info("Pi Camera Grabber Service created successfully.")
            return image_grab_service
        except Exception as e:
            raise FactoryException("Failed to create Pi Camera Grabber Service.", e)