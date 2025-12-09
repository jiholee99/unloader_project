from exceptions.exception import InspectionStepException
from adapters.image_analysis.contour_validator import ContourValidator
from core.interfaces import InspectionStep
from model.contour import Contour

class IsContourRectangular(InspectionStep):
    def execute(self, contour, angle_tolerance=10) -> bool:
        """
        Check if the given contour is approximately rectangular.
        Returns True if rectangular, False otherwise.
        """
        try:
            return ContourValidator.is_rectangle(contour, angle_tolerance)
        except Exception as e:
            raise InspectionStepException("Failed to analyze contour for rectangularity during contour analysis step.", e)
        

def isContourRollerShape(contour : Contour, shape_detection_options:dict) -> float:
    """
    Using cutoff options, determine if the contour matches roller shape criteria.
    Will use weights and cutoffs defined in shape_detection_options.
    Returns float value of the contour.
    """
    score = 0.0
    # Check area
    area = contour.area
    area_weight = shape_detection_options["area"]["weight"]
    area_cutoff = shape_detection_options["area"]["cutoff"]
    area_max = shape_detection_options["area"]["max_area"]
    area_normalized = min(area / area_max, 1.0)
    if area >= area_cutoff:
        score += area_weight * area_normalized
    
    # Check Solidity
    solidity = contour.solidity
    solidity_weight = shape_detection_options["solidity"]["weight"]
    solidity_cutoff = shape_detection_options["solidity"]["cutoff"]
    if solidity >= solidity_cutoff:
        score += solidity_weight * solidity
    
    # Check Extent
    extent = contour.extent
    extent_weight = shape_detection_options["extent"]["weight"]
    extent_cutoff = shape_detection_options["extent"]["cutoff"]
    if extent >= extent_cutoff:
        score += extent_weight * extent
    
    return score