import argparse
from main import main
from app.factories import CameraGrabberFactory, FileGrabberFactory
# If you have PiCamera:
# from adapters.picamera_grabber import PiCameraGrabberFactory

def start():
    parser = argparse.ArgumentParser(prog="rollerapp")
    parser.add_argument(
        "mode",
        choices=["camera", "file", "picamera"]
    )
    args = parser.parse_args()

    # decide which factory to use
    if args.mode == "camera":
        factory = CameraGrabberFactory
        print("Using CameraGrabberFactory")
    elif args.mode == "picamera":
        # from adapters.picamera_grabber import PiCameraGrabberFactory
        # factory = PiCameraGrabberFactory
        pass
    else:
        factory = FileGrabberFactory

    # pass factory into the app
    main(grabber_factory=factory)

if __name__ == "__main__":
    print("__main_.py module running...")
