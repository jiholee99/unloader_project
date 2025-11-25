from typing import Protocol

class InspectionStep(Protocol):
    def execute(self, *args, **kwargs) -> any:
        """Execute the inspection step on the provided data."""
        ...