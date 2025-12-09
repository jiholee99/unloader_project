import requests
import os

MINIPC_IP = "100.72.68.126"  # Your mini-PC Tailscale IP
MINIPC_PORT = 5000

def upload_file(device, file_path):
    url = f"http://{MINIPC_IP}:{MINIPC_PORT}/upload/{device}"
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            r = requests.post(url, files=files, timeout=5)
        if r.status_code == 200:
            print(f"[{device}] Uploaded {file_path}")
        else:
            print(f"[{device}] Upload failed: {r.status_code}")
    except Exception as e:
        print(f"[{device}] Upload error: {e}")


upload_file(r"a\b","./__init__.py")
