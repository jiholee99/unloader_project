from exceptions.exception import ImageUploadException
from utils.logger import get_logger
from core.interfaces.uploader import Uploader

class ImageUploaderService:
    def __init__(self, uploader_repository : Uploader, config: dict):
        self.uploader_repository = uploader_repository
        self.config = config
        self.logger = get_logger("ImageUploaderService")

    def _list_files_in_directory(self, directory_path: str) -> list:
        import os
        try:
            files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            return files
        except Exception as e:
            raise ImageUploadException("Error listing files in directory", e)

    def upload(self, dest_path:str) -> bool:
        try:
            # Get 3 saved images paths
            image_folder_path = self.config.get("path", "./assets/saved_images/")
            for file_path in self._list_files_in_directory(image_folder_path):
                self.uploader_repository.upload_single_file(dest_path=dest_path, file_path=file_path)
            return True
        except Exception as e:
            raise ImageUploadException("Image upload failed in ImageUploaderService.", e)