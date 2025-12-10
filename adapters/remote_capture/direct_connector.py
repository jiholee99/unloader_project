#!/usr/bin/env python3
"""
Master Raspberry Pi - Captures photos and signals multiple slaves via HTTP server
"""

import time
import requests
from adapters.remote_capture.server import Server
from utils.logger import get_logger

class DirectConnector:
    def __init__(self, config: dict):
        """
        server_url : URL of the signal server (Flask)
        photo_dir  : directory to store photos
        slaves     : dict like {"slave1": True, "slave2": False}
        """
        self.server_url = config.get("server_url","http://192.168.1.95:5000/signal")
        self.photo_dir = config.get("photo_dir",  "/home/lgvision/Pictures/master_photos/")
        self.slaves = config.get("slaves", {"slave1" : False, "slave2" : True})
        
        self.slave1_dir = config.get("slave1_dir","/home/lgvision/Pictures/slave_uploads/slave1/")
        self.slave2_dir = config.get("slave2_dir","/home/lgvision/Pictures/slave_uploads/slave2/")
        self.slave1_url = ""
        self.slave2_url = ""
        self.logger = get_logger()
    # ------------------------- SIGNAL --------------------------------

    def __build_payload(self):
        """Only enabled slaves get True trigger."""
        return {sid: True for sid, enabled in self.slaves.items() if enabled}
    
    def __build_payload_False(self):
        """Only enabled slaves get True trigger."""
        return {sid: False for sid, enabled in self.slaves.items() if enabled}

    def __send_trigger_signal(self):
        """Send trigger signal to all enabled slaves."""
        try:
            payload = self.__build_payload()
            self.logger.debug("Sending trigger to slaves:", payload)
            response = requests.post(self.server_url, json=payload)
            self.logger.debug("Waiting response...")
            
            while True:
                if response.json():
                    break
            self.logger.debug("Server response:", response.json())
            return True

        except Exception as e:
            self.logger.debug("Error sending signal:", e)
            return False
    
    # Use this function to trigger signal        
    def signal_to_slaves(self):
        try:
            server = Server()
            server.start()
            self.logger.debug("\nTriggering slaves...")
            if self.__send_trigger_signal():
                self.logger.debug("✓ Synchronized capture triggered!\n")
                # Wait for latest update
                while True:
                    if requests.post(self.server_url, json = self.__build_payload_False()):
                        break
                time.sleep(1)
            else:
                self.logger.debug("✗ Failed to trigger slaves\n")
        except Exception as e:
            self.logger.debug(f"Error in call_slave: {e}")
        finally:
            if server:
                server.stop()

    def _retrieve_photos(self, url):
        """Retrieve photos from slaves - Not implemented yet."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.logger.debug(f"Photos retrieved successfully from {url}")
            else:
                self.logger.debug(f"Failed to retrieve photos from {url}, Status code: {response.status_code}")
                return False
        except Exception as e:
            self.logger.debug(f"Error retrieving photos from {url}: {e}")

    def _save_photos(self, file):
        """Save photos to local directory - Not implemented yet."""
        pass
