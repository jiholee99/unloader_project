import requests
import os
from exceptions.exception import ImageUploadException
from utils.logger import get_logger
from core.interfaces.uploader import Uploader

class MiniPCUploader(Uploader):
    def __init__(self, minipc_ip="100.72.68.126", minipc_port=5000):
        self.minipc_ip = minipc_ip
        self.minipc_port = minipc_port
        self.logger = get_logger()

    def upload_single_file(self, dest_path, file_path):
        url = f"http://{self.minipc_ip}:{self.minipc_port}/upload/{dest_path}"
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                r = requests.post(url, files=files, timeout=5)
            if r.status_code == 200:
                self.logger.info(f"File Upload complete. File ({file_path}) Path ({dest_path})")
            else:
                raise ImageUploadException(f"Upload failed with status code {r.status_code}")
        except Exception as e:
            raise ImageUploadException(f"Upload error for {file_path}", e)

    def upload_multiple_files(self, dest_path, file_path):
        raise NotImplementedError("Multiple file upload not implemented yet.")