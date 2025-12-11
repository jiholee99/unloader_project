#!/usr/bin/env python3
"""
Master Raspberry Pi - Captures photos and signals multiple slaves via HTTP server
"""

import time
import requests
from adapters.remote_capture.server import Server
from utils.logger import get_logger
from exceptions.exception import RemoteCaptureException

class UrlRequestor:
    def __init__(self, config: dict):
        """
        server_url : URL of the signal server (Flask)
        photo_dir  : directory to store photos
        slaves     : dict like {"slave1": True, "slave2": False}
        """
        self.save_path = config.get("save_path",  "/home/lgvision/Pictures/master_photos/")
        self.slave1_url = config.get("slave1_url", None)
        self.slave2_url = config.get("slave2_url", None)
        self.logger = get_logger()
    
    def _retrieve_photos(self, url) -> bytes :
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise RemoteCaptureException(f"Failed to retrieve photos from {url} | Status code: {response.status_code}")
                
            self.logger.debug(f"Photos retrieved successfully from {url}")
            return response.content
        except Exception as e:
            raise RemoteCaptureException(f"Error retrieving photos from {url}", e)

    def _save_photos(self, file, filename):
        """Save photos to local directory - Not implemented yet."""
        import os
        try:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            filepath = os.path.join(self.save_path, filename)
            with open(filepath, 'wb') as f:
                f.write(file)
            self.logger.debug(f"Photo saved successfully at {filepath}")
        except Exception as e:
            raise RemoteCaptureException("Error saving photo", e)
    
    def request_photos_from_slaves(self) -> bool:
        """Request photos from slaves with retries that do not break the loop."""
        if not self.slave1_url or not self.slave2_url:
            raise RemoteCaptureException("Slave URLs are not properly configured.")

        max_retries = 3
        retry_delay = 2  # seconds

        slave1_success = False
        slave2_success = False
        slave_1_file = None
        slave_2_file = None

        for attempt in range(max_retries):
            self.logger.debug(f"Attempt {attempt + 1}/{max_retries} to request photos.")

            # ----------------------------
            # SLAVE 1
            # ----------------------------
            try:
                slave_1_file = self._retrieve_photos(self.slave1_url)
                slave1_success = True
                self.logger.debug("Slave 1 photo retrieved successfully.")
            except Exception as e:
                self.logger.error(f"Slave 1 failed on attempt {attempt+1}: {e}")

            # ----------------------------
            # SLAVE 2
            # ----------------------------
            try:
                slave_2_file = self._retrieve_photos(self.slave2_url)
                slave2_success = True
                self.logger.debug("Slave 2 photo retrieved successfully.")
            except Exception as e:
                self.logger.error(f"Slave 2 failed on attempt {attempt+1}: {e}")

            # If both are done, stop early
            if slave1_success and slave2_success:
                self._save_photos(slave_1_file, "slave1_photo.jpeg")
                self._save_photos(slave_2_file, "slave2_photo.jpeg")
                return True

            time.sleep(retry_delay)

        # After retries, check results
        if not slave1_success or not slave2_success:
            raise RemoteCaptureException(
                f"Failed: Slave1={slave1_success}, Slave2={slave2_success}"
            )

        return True

