from core.image_grab import ImageGrabService
from adapters.image_grab import FileGrabber

from exceptions.exception import FactoryException

from utils.logger import get_logger

logger = get_logger("Grabber Factory")

class FileGrabberFactory:
    @staticmethod
    def create():
        try:
            logger.info("Creating File Grabber Service...")
            # file_grabber = FileGrabber(config={"image_path": r"assets\test_images\full.jpeg"})
            file_grabber = FileGrabber(config={"image_path": r"assets/test_images/full.jpeg"})

            image_grab_service = ImageGrabService(grabber=file_grabber)
            logger.info("File Grabber Service created successfully.")
            return image_grab_service
        except Exception as e:
            raise FactoryException("Failed to create File Grabber Service.", e)
        
