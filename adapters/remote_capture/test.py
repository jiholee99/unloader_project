import time
from datetime import datetime
from picamera2 import Picamera2
from adapters.remote_capture.direct_connector import DirectConnector

# ---------------- Camera functions ----------------

def initialize_camera():
    print("Initializing master camera...")
    camera = Picamera2()
    camera.configure(camera.create_still_configuration())
    camera.start()
    time.sleep(2)
    print("Master camera ready.\n")
    return camera  # return camera object


def take_photo(camera, filename, count):
    print(f"Master taking photo: {filename}")
    camera.capture_file(filename)
    print("Master photo saved.")


def run_loop(master, camera):
    counter = 0
    try:
        while True:
            input("Press Enter to capture synchronized photos...")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            master_filename = f"{master.photo_dir}master_{timestamp}_{counter}.jpg"

            # Take master photo
            take_photo(camera, master_filename, counter)
            counter += 1

            # Trigger slaves
            master.signal_to_slaves()

            # Upload files
            master.mini_pc_upload_from_master_and_slaves("Unloader1",master_filename)

    except KeyboardInterrupt:
        print("\nMaster shutting down...")
    finally:
        if camera:
            camera.stop()
            camera.close()


# ---------------- Main ----------------

def main():
    SERVER_URL = "http://192.168.1.95:5000/signal"
    PHOTO_DIR = "/home/lgvision/Pictures/master_photos/"
    SLAVE1_DIR = "/home/lgvision/Pictures/slave_uploads/slave1/"
    SLAVE2_DIR = "/home/lgvision/Pictures/slave_uploads/slave2/"

    SLAVES = {"slave1": False, "slave2": True}

    # Create Master
    master = DirectConnector(SERVER_URL, PHOTO_DIR, SLAVE1_DIR, SLAVE2_DIR, SLAVES)

    # Initialize camera
    camera = initialize_camera()

    # Start main loop
    run_loop(master, camera)


if __name__ == "__main__":
    main()
