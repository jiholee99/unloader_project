from typing import Protocol, Any, Dict, List

class InspectionTask(Protocol):

    @property
    def name(self) -> str:
        """Human-readable name of the task."""
        ...

    def create_pipeline(self) -> List[Any]:
        """Return a list of steps (preprocess, ML, postprocess)."""
        ...

    def perform_inspection(self, image: Any) -> Dict:
        """Run pipeline on image and return results."""
        ...

    def get_results(self) -> Dict:
        """Return last inspection results."""
        ...

    def reset(self) -> None:
        """Clear internal state."""
        ...
