#!/usr/bin/env python3
"""
Master Raspberry Pi - Captures photos and signals multiple slaves via HTTP server
"""

import time
import requests
from server_miniPC.upload_to_minipc import upload_file
from get_file import get_latest_file
from server import Server
from utils.logger import get_logger

class Master:
    def __init__(self, slaves: dict, config: dict):
        """
        server_url : URL of the signal server (Flask)
        photo_dir  : directory to store photos
        slaves     : dict like {"slave1": True, "slave2": False}
        """
        self.server_url = config.get("config","http://192.168.1.95:5000/signal")
        self.photo_dir = config.get("photo_dir",  "/home/lgvision/Pictures/master_photos/")
        self.slaves = config.get("slaves", {"slave1" : False, "slave2" : True})
        self.slave1_dir = config.get("slave1_dir","/home/lgvision/Pictures/slave_uploads/slave1/")
        self.slave2_dir = config.get("slave2_dir","/home/lgvision/Pictures/slave_uploads/slave2/")
        self.logger = get_logger()
    # ------------------------- SIGNAL --------------------------------

    def __build_payload(self):
        """Only enabled slaves get True trigger."""
        return {sid: True for sid, enabled in self.slaves.items() if enabled}

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
                time.sleep(5)
            else:
                self.logger.debug("✗ Failed to trigger slaves\n")
        except Exception as e:
            self.logger.debug(f"Error in call_slave: {e}")
        finally:
            if server:
                server.stop()
    
    # ------------------------ Mini PC Upload --------------------------
    # Use this function to upload to Mini PC
    def mini_pc_upload_from_master_and_slaves(self, folder, master_filename):
        
        upload_file(folder, master_filename)
        #slave1_filename = get_latest_file(self.slave1_dir)
        slave2_filename = get_latest_file(self.slave2_dir)
                
        #upload_file(folder, slave1_filename)
        upload_file(folder, slave2_filename)

