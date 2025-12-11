import requests
import os
from exceptions.exception import ImageUploadException
from utils.logger import get_logger
from core.interfaces.uploader import Uploader
import time

class MiniPCUploader(Uploader):
    def __init__(self, config: dict):
        try:
            self.minipc_ip = config["minipc_ip"]
            self.minipc_port = config["minipc_port"]
            self.logger = get_logger("MiniPCUploader")    
        except Exception as e:
            raise ImageUploadException("Failed to initialize MiniPCUploader with given config.", e)
        
    def send_complete_status(self, file_paths):
        try:
            json_payload = {
                "status": "complete",
                "file_paths": file_paths
            }
            url = f"http://{self.minipc_ip}:{self.minipc_port}/send_photo"
            response = requests.post(url, json=json_payload)
            if response.status_code != 200:
                raise ImageUploadException(f"Failed to send complete status, server responded with status code {response.status_code}")
        except Exception as e:
            raise ImageUploadException("Failed to send complete status to MiniPC.", e)
        return True
        
    def upload_single_file(self, dest_path, file_path):
        url = f"http://{self.minipc_ip}:{self.minipc_port}/upload/{dest_path}"
        max_retries = 3
        retry_delay = 2  # seconds
        # Track success
        upload_success = False
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(f"[Attempt {attempt}/{max_retries}] Uploading {file_path} → {dest_path}")

                with open(file_path, "rb") as f:
                    files = {"file": (os.path.basename(file_path), f)}
                    r = requests.post(url, files=files, timeout=5)

                if r.status_code == 200:
                    self.logger.info(f"Upload complete: {file_path} → {dest_path}")
                    upload_success = True
                    break   # stop retrying
                else:
                    self.logger.error(
                        f"Upload failed with status code {r.status_code} for {file_path}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Upload attempt {attempt} failed for {file_path} → {e}"
                )

            # Wait before next retry (except after last attempt)
            if attempt < max_retries:
                time.sleep(retry_delay)

        # Final result check
        if not upload_success:
            self.logger.error(
                f"Upload failed after {max_retries} attempts for file: {file_path}"
            )
            return False
            

        return True

    def upload_multiple_files(self, dest_path, file_path_list):
        raise NotImplementedError("Method not implemented yet.")