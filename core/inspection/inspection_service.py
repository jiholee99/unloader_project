import cv2
#Exceptions
from exceptions.exception import InspectionException
# Core Services
from core.inspection.image_process import ImagePreprocessService, ImagePostProcessorService
from core.interfaces import InspectionTask
import numpy as np

# Utils
from utils.logger import get_logger
from utils.visual_debugger import show_scaled

class InspectionService:
    def __init__(self, inspection_tasks : list[InspectionTask]):
        self.logger = get_logger()
        self.inspection_tasks = inspection_tasks

    def _is_roller(self):
        pass

    def _is_close(self):
        pass
    

    def inspect(self, image : np.ndarray):
        try:
            orginal_image = image.copy()
            for task in self.inspection_tasks:
                task.perform_inspection(image)
                image = task.get_results()
            self.logger.info("Inspection completed successfully.")
            show_scaled("Original Image", orginal_image)
            show_scaled("Final Inspection Image", image)
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            roller_status = self._is_roller()
            close_status = self._is_close()
        except Exception as e:
            raise InspectionException("Inspection process error occurred.", e)
        

        pass


if __name__ == "__main__":
    # service = InspectionService()
    # service.inspect()
    print("Inspection Service Module")