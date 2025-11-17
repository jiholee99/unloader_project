class AppException(Exception):
    """Base class for all custom exceptions in the application."""
    def __init__(self, message="An error occurred in the application.", original_exception=None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return self.message + (f" -> {str(self.original_exception) if self.original_exception else ''}")

class ImageLoadException(AppException):
    """Exception raised when an image fails to load."""
    def __init__(self, message="Image loading error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class ImagePreProcessServiceException(AppException):
    """Exception raised during image processing errors."""
    def __init__(self, message="Image preprocessing error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class ImagePreProcessorException(AppException):
    """Exception raised during image preprocessing errors."""
    def __init__(self, message="Image Pre_Processor error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class ImagePostProcessingException(AppException):
    """Exception raised during image post-processing errors."""
    def __init__(self, message="Image post-processing error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class DistanceValidationException(AppException):
    """Exception raised during distance validation errors."""
    def __init__(self, message="Distance validation error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class AppConfigException(AppException):
    """Exception raised for application configuration errors."""
    def __init__(self, message="Application configuration error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class ImageGrabException(AppException):
    """Exception raised during image grabbing errors."""
    def __init__(self, message="Image grabbing error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class InspectionException(AppException):
    """Exception raised during inspection process errors."""
    def __init__(self, message="Inspection process error occurred.", original_exception=None):
        super().__init__(message, original_exception)

class SequenceException(AppException):
    """Exception raised during sequence execution errors."""
    def __init__(self, message="Sequence execution error occurred.", original_exception=None):
        super().__init__(message, original_exception)