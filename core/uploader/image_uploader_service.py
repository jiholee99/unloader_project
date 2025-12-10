from exceptions.exception import ImageUploadException
from utils.logger import get_logger
from core.interfaces.uploader import Uploader

class ImageUploaderService:
    def __init__(self, uploader_repository : Uploader):
        self.uploader_repository = uploader_repository
        self.logger = get_logger("ImageUploaderService")

    def upload(self, dest_path:str, file_path: str) -> bool:
        try:
            self.uploader_repository.upload_single_file(dest_path=dest_path, file_path=file_path)
            return True
        except Exception as e:
            raise ImageUploadException("Image upload failed in ImageUploaderService.", e)