from core.interfaces.inspection_task import InspectionTask

from core.inspection.steps import BinaryMaskGenerationStep, CropROIGenerationStep
class RollerPositionInspectionTask(InspectionTask):
    @property
    def name(self) -> str:
        return "Roller Position Inspection Task"

    def create_pipeline(self):
        raise NotImplementedError("Pipeline creation not implemented yet.")

    def perform_inspection(self, image):
        # 1. Crop ROI
        cropped_image = CropROIGenerationStep().execute(image, roi_coords=[0, 0, 100, 100])  # Example ROI coordinates
        # 2. Generate Binary Mask
        binary_mask = BinaryMaskGenerationStep().execute(cropped_image)
        raise NotImplementedError("Inspection performance not implemented yet.")

    def get_results(self):
        raise NotImplementedError("Get results not implemented yet.")

    def reset(self) -> None:
        raise NotImplementedError("Reset not implemented yet.")