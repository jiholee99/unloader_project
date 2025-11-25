from exceptions.exception import InspectionStepException
from core.interfaces import InspectionStep
from adapters.image_process import ImagePostProcessor

class FillHolesStep(InspectionStep):
    def execute(self, maks_image) -> any:
        """
        Fill holes in the given binary mask.
        Returns the mask with holes filled.
        """
        try:
            result = ImagePostProcessor.fill_holes_in_mask(maks_image)
            return result
        except Exception as e:
            raise InspectionStepException("Failed to fill holes during fill holes step.", e)
        

class GetContoursStep(InspectionStep):
    def execute(self, mask_image) -> any:
        """
        Detect contours in the given binary mask.
        Returns the list of detected contours.
        """
        try:
            contours = ImagePostProcessor.detect_contours(mask_image)
            return contours
        except Exception as e:
            raise InspectionStepException("Failed to detect contours during contour detection step.", e)
        
class GetContourInfoStep(InspectionStep):
    def execute(self, contours : list) -> any:
        """
        Get detailed information about a given contour.
        Returns a dictionary with contour properties.
        """
        try:
            from adapters.image_process import ContourProcessor
            contours_info = []
            for contour in contours:
                info = ContourProcessor.get_contour_info(contour)
                contours_info.append(info)
            return contours_info
        except Exception as e:
            raise InspectionStepException("Failed to get contour info during contour info step.", e)