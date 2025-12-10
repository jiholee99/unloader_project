#!/usr/bin/env python3
"""
Master Raspberry Pi - Captures photos and signals multiple slaves via HTTP server
"""

import time
import requests
# from picamera2 import Picamera2
from datetime import datetime
# from adapters.image_uploader.default_uploader import upload_file
# from get_file import get_latest_file

from utils.logger import get_logger

class Master:
    def __init__(self, master_config : dict):
        """
        server_url : URL of the signal server (Flask)
        photo_dir  : directory to store photos
        slaves     : dict like {"slave1": True, "slave2": False}
        """
        self.server_url : str  = master_config.get("server_url", "")
        self.photo_dir : str = master_config.get("photo_dir", "")
        self.slaves = master_config.get("slaves", {})
        self.slave1_dir = master_config.get("slave1_dir", "")
        self.slave2_dir = master_config.get("slave2_dir", "")
        self.slaves = master_config.get("slaves", {})
        self.camera = None
        self.counter = 0
        self.logger = get_logger()

    # ------------------------- CAMERA --------------------------------

    # def initialize_camera(self):
    #     print("Initializing master camera...")
    #     self.camera = Picamera2()
    #     self.camera.configure(self.camera.create_still_configuration())
    #     self.camera.start()
    #     time.sleep(2)
    #     print("Master camera ready.\n")

    # def take_photo(self, filename, count):
    #     print(f"Master taking photo: {filename, count}")
    #     self.camera.capture_file(filename)
    #     print("Master photo saved.")

    # ------------------------- SIGNAL --------------------------------

    def build_payload(self):
        """Only enabled slaves get True trigger."""
        return {sid: True for sid, enabled in self.slaves.items() if enabled}

    def send_trigger_signal(self):
        """Send trigger signal to all enabled slaves."""
        try:
            payload = self.build_payload()
            self.logger.debug(f"Sending trigger to slaves: {payload}")

            response = requests.post(self.server_url, json=payload)
            self.logger.debug(f"Server response: {response.json()}")
            return True

        except Exception as e:
            self.logger.debug(f"Error sending signal: {e}")
            return False

    # ------------------------- MAIN LOOP ------------------------------

    # def run_loop(self):
    #     """Press Enter to trigger synchronized captures."""
    #     try:
    #         while True:
    #             input("Press Enter to capture synchronized photos...")

    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             master_filename = f"{self.photo_dir}master_{timestamp}_{self.counter}.jpg"

    #             # Master photo
    #             self.take_photo(master_filename, self.counter)
    #             self.counter += 1
                
    #             # Notify slaves
    #             print("\nTriggering slaves...")
    #             if self.send_trigger_signal():
    #                 print("✓ Synchronized capture triggered!\n")
    #             else:
    #                 print("✗ Failed to trigger slaves\n")
                    
    #             # upload to mini PC
    #             upload_file("master", master_filename)
                
    #             # Files from slave
    #             while True:
    #                 signals = requests.get(self.server_url).json() 
    #                 slave1_done = (signals.get("slave1") == False) 
    #                 slave2_done = (signals.get("slave2") == False)
    #                 if slave1_done and slave2_done: 
    #                     break 
    #                 time.sleep(0.1)
                    
    #             slave1_filename = get_latest_file(self.slave1_dir)
    #             slave2_filename = get_latest_file(self.slave2_dir)
                
    #             upload_file("master", slave1_filename)
    #             upload_file("master", slave2_filename)
                

    #     except KeyboardInterrupt:
    #         print("\nMaster shutting down...")
    #     finally:
    #         if self.camera:
    #             self.camera.stop()
    #             self.camera.close()


# --------------------------- ENTRY POINT ------------------------------

def main():
    SERVER_URL = "http://192.168.1.42:5000/signal"
    PHOTO_DIR = "/home/lgvision/Pictures/master_photos/"
    SLAVE1_DIR = "/home/lgvision/Pictures/slave_uploads/slave1/"
    SLAVE2_DIR = "/home/lgvision/Pictures/slave_uploads/slave2/"

    SLAVES = {
        "slave1": True,
        "slave2": True,
        "slave3": False
    }

    temp_config = {
        "server_url": SERVER_URL,
        "photo_dir": PHOTO_DIR,
        "slave1_dir": SLAVE1_DIR,
        "slave2_dir": SLAVE2_DIR,
        "slaves": SLAVES
    }

    master = Master(temp_config)
    # master.initialize_camera()
    # master.run_loop()


if __name__ == "__main__":
    main()
