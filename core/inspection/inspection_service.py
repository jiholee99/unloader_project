import cv2
#Exceptions
from exceptions.exception import InspectionException
# Core Services
from core.inspection.image_process import ImagePreprocessService, ImagePostProcessorService
from core.interfaces import InspectionTask
import numpy as np
from ui.debug_view import DebugImageViewer
# Utils
from utils.logger import get_logger
from utils.visual_debugger import show_scaled, overlay_filled_contours
from utils.pyside_viewer import start_image_viewer

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
            self.logger.info("Starting inspection process...")
            orginal_image = image.copy()
            for task in self.inspection_tasks:
                task.perform_inspection(image)
                result = task.get_results()
            self.logger.info("Inspection completed successfully.")

            viewer = start_image_viewer()
            viewer.show_image("raw",orginal_image)
            viewer.show_image("processed",result["binary_mask"])
            viewer.show_image("overlay",overlay_filled_contours(image=orginal_image,contours=result["contours"],random_colors=True, roi=result["roi"]))

            # show_scaled("Original Image", orginal_image)
            # show_scaled("Final Inspection Image", result["binary_mask"])

            # show_scaled("contours", overlay_filled_contours(image=orginal_image,contours=result["contours"],random_colors=True, roi=result["roi"]))
            # cv2.waitKey(1)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            roller_status = self._is_roller()
            close_status = self._is_close()
        except Exception as e:
            raise InspectionException("Inspection process error occurred.", e)
        
    def debug_save_image(self, image: np.ndarray):
        cv2.imwrite("assets/test_images/grabbed_image.jpeg", image)


if __name__ == "__main__":
    # service = InspectionService()
    # service.inspect()
    print("Inspection Service Module")