from adapters.image_process import ImagePreprocessor, ImagePostProcessor
from adapters.config import AppConfigAdapter
from core.inspection import ImagePreprocessService, ImagePostProcessorService, InspectionService
from core.inspection.inspection_task import RollerDetectionInspectionTask
from exceptions.exception import FactoryException

from utils.logger import get_logger

logger = get_logger("Factory")

class InspectionFactory:
    @staticmethod
    def create():
        try:
            logger.info("Creating Inspection Service...")
            config = AppConfigAdapter()
            roller_close_task = RollerDetectionInspectionTask()
            logger.info("Inspection Service created successfully.")
            return InspectionService([roller_close_task])
        except Exception as e:
            raise FactoryException("Failed to create Inspection Service.", e)
