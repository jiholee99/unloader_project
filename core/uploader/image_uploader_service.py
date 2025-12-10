from exceptions.exception import ImageUploadException
from utils.logger import get_logger

class ImageUploaderService:
    def __init__(self, uploader_repository):
        self.uploader_repository = uploader_repository
        self.logger = get_logger("ImageUploaderService")

    def upload(self, file_path: str) -> bool:
        self.logger.info(f"Uploading image from {file_path}...")
        raise ImageUploadException("Image upload service is not implemented yet.")