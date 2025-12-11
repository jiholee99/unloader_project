import argparse
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread
from PySide6.QtCore import Qt
from exceptions.exception import AppException
from test import viewer
from utils.logger import get_logger
from app.runner import Runner
from utils.pyside_viewer import start_image_viewer   # <-- your viewer file
from ui import *
from core import app_state
from adapters.config import AppConfigAdapter

class RunnerThread(QThread):
    def __init__(self, runner):
        super().__init__()
        self.runner = runner
        self.stop_requested = False

    def request_stop(self):
        self.stop_requested = True

    def run(self):
        config = AppConfigAdapter().load_loop_delay()
        while not self.stop_requested:
            self.runner.run_once()   # <-- modify Runner below
            self.msleep(int(config * 1000))  # sleep expects milliseconds



def parse_args():
    parser = argparse.ArgumentParser(description="Roller Inspection Controller")

    parser.add_argument("-picamera", action="store_true", help="Use Picamera as grabber")
    parser.add_argument("-camera", action="store_true", help="Use USB camera as grabber")
    parser.add_argument("-file", action="store_true", help="Use file grabber")

    parser.add_argument("-testseq", action="store_true", help="Run test sequence")
    parser.add_argument("-imgcptseq", action="store_true", help="Run image capture sequence")

    return parser.parse_args()


def main():
    logger = get_logger("Main")
    args = parse_args()

    # ------------------------------------------
    # 1. Start Qt (must be main thread)
    # ------------------------------------------
    app = QApplication(sys.argv)

    model = ViewerModel()
    view = ViewerView(model=model)
    view.setWindowFlag(Qt.Window)     # <— forces it to be a real window
    controller = ViewerController(model, view)

    # ------------------------------------------
    # 2. Start your PySide image viewer
    # ------------------------------------------    
    app_state.controller = controller
    view.show()


    # ------------------------------------------
    # 3. Create Runner and launch it in a thread
    # ------------------------------------------
    try:
        runner = Runner(args)
        runner_thread = RunnerThread(runner)
        controller.runner_thread = runner_thread
        runner_thread.start()

    except AppException as e:
        logger.error(f"{e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    # ------------------------------------------
    # KEEP GUI RUNNING
    # ------------------------------------------
    logger.info("------ Application started ------")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
