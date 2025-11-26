from core.interfaces.inspection_task import InspectionTask

from core.inspection.steps import *
from adapters.config import AppConfigAdapter
from exceptions.exception import InspectionTaskException
from utils.logger import get_logger
from utils.visual_debugger import overlay_filled_contours
import cv2


class RollerPositionInspectionTask(InspectionTask):
    def __init__(self):
        self.result = None
        self.logger = get_logger(self.name)
        self.return_data = {}

    @property
    def name(self) -> str:
        return "Roller Position Inspection Task"

    def create_pipeline(self):
        raise NotImplementedError("Pipeline creation not implemented yet.")

    def _preprocess(self, image, config):
        # Optional remove bright line step
        if config.get("use_remove_bright_line", False):
            image = RemoveBrightLineStep().execute(image, orientation="horizontal")

        # 1. Crop ROI
        image = GrayScaleConversionStep().execute(image)
        roi = config["crop_roi"]
        cropped_image = CropROIGenerationStep().execute(
            image, roi_coords=[roi["x"], roi["y"], roi["w"], roi["h"]]
        )
        self.return_data["cropped_image"] = cropped_image
        self.return_data["roi"] = [roi["x"], roi["y"], roi["w"], roi["h"]]

        # 2. Generate Binary Mask
        min_threshold = config.get("min_threshold", 100)
        max_threshold = config.get("max_threshold", 255)
        binary_mask = BinaryMaskGenerationStep().execute(
            cropped_image, min_threshold=min_threshold, max_threshold=max_threshold
        )

        return binary_mask

    def _postprocess(self, binary_mask, config):
        # Optional Fill holes
        if config.get("use_fill_holes", False):
            binary_mask = FillHolesStep().execute(binary_mask)
            self.return_data["filled_mask"] = binary_mask

        # 1. Detect Contours and save results
        min_area = config.get("min_contour_area", 50000)
        contours = GetContoursStep().execute(binary_mask, min_area=min_area)
        self.return_data["contours"] = contours
        # 2. Log Contour Info
        contours_info = GetContourInfoStep().execute(contours)
        self.return_data["contours_info"] = contours_info

        self.return_data["contours"] = contours

        self.logger.info(
            f"Total contours detected: {self.return_data['contours_info']}"
        )

        self.logger.info(f"contours : {self.return_data['contours']}")

    def perform_inspection(self, image):
        try:
            orginal_image = image.copy()
            self.logger.info(f"Performing {self.name}...")
            # 0. Load Config
            config = AppConfigAdapter().load_roller_close_task_options()

            binary_mask = self._preprocess(image, config)
            self.return_data["binary_mask"] = binary_mask

            self._postprocess(binary_mask, config)

            self.logger.info(f"{self.name} completed successfully.")

        except Exception as e:
            raise InspectionTaskException(
                f"{self.name} : Failed to perform roller position inspection.", e
            )

    def get_results(self):
        return self.return_data

    def reset(self) -> None:
        raise NotImplementedError("Reset not implemented yet.")


