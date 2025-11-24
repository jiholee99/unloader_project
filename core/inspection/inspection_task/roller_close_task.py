from core.interfaces.inspection_task import InspectionTask

from core.inspection.steps import BinaryMaskGenerationStep, CropROIGenerationStep, RemoveBrightLineStep, GrayScaleConversionStep
from adapters.config import AppConfigAdapter
from exceptions.exception import InspectionTaskException
from utils.logger import get_logger

class RollerPositionInspectionTask(InspectionTask):
    def __init__(self):
        self.result = None
        self.logger = get_logger(self.name)

    @property
    def name(self) -> str:
        return "Roller Position Inspection Task"

    def create_pipeline(self):
        raise NotImplementedError("Pipeline creation not implemented yet.")

    def perform_inspection(self, image):
        try:
            self.logger.info(f"Performing {self.name}...")
            # 0. Load Config
            config = AppConfigAdapter().load_roller_close_task_options()
            # 1. Crop ROI
            image = GrayScaleConversionStep().execute(image)
            roi = config["crop_roi"]
            cropped_image = CropROIGenerationStep().execute(image, roi_coords=[roi["x"], roi["y"], roi["w"], roi["h"]])
            # 2. Generate Binary Mask
            min_threshold = config.get("min_threshold", 100)
            max_threshold = config.get("max_threshold", 255)
            binary_mask = BinaryMaskGenerationStep().execute(cropped_image, min_threshold=min_threshold, max_threshold=max_threshold)
            
            # 3. Optional remove bright line step
            if config.get("use_remove_bright_line", False):
                binary_mask = RemoveBrightLineStep().execute(binary_mask, orientation='horizontal')
            self.result = binary_mask
            
            self.logger.info(f"{self.name} completed successfully.")
            
        except Exception as e:
            raise InspectionTaskException(f"{self.name} : Failed to perform roller position inspection.", e)
        

    def get_results(self):
        return self.result

    def reset(self) -> None:
        raise NotImplementedError("Reset not implemented yet.")