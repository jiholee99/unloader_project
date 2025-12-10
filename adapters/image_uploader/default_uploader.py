import requests
import os
from exceptions.exception import ImageUploadException
from utils.logger import get_logger

# MINIPC_IP = "100.72.68.126"  # Your mini-PC Tailscale IP
# MINIPC_PORT = 5000

# def upload_file(device, file_path):
#     url = f"http://{MINIPC_IP}:{MINIPC_PORT}/upload/{device}"
#     try:
#         with open(file_path, "rb") as f:
#             files = {"file": (os.path.basename(file_path), f)}
#             r = requests.post(url, files=files, timeout=5)
#         if r.status_code == 200:
#             print(f"[{device}] Uploaded {file_path}")
#         else:
#             print(f"[{device}] Upload failed: {r.status_code}")
#     except Exception as e:
#         print(f"[{device}] Upload error: {e}")


class DefaultUploader:
    def __init__(self, minipc_ip="100.72.68.126", minipc_port=5000):
        self.minipc_ip = minipc_ip
        self.minipc_port = minipc_port
        self.logger = get_logger()

    def upload_single_file(self, path, file_path):
        url = f"http://{self.minipc_ip}:{self.minipc_port}/upload/{path}"
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                r = requests.post(url, files=files, timeout=5)
            if r.status_code == 200:
                self.logger.info(f"[{path}] Uploaded {file_path}")
            else:
                self.logger.error(f"[{path}] Upload failed: {r.status_code}")
        except Exception as e:
            raise ImageUploadException(f"Upload error for {file_path}", e)
