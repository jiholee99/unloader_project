import time
from app.sequence import Sequence
from test.test_sequence import TestSequence
from adapters.config import AppConfigAdapter
from utils.logger import get_logger
from app.factories import InspectionFactory, CameraGrabberFactory, FileGrabberFactory, PiCameraGrabberFactory
from exceptions.exception import RunnerException
from core import app_state

class Runner:
    def __init__(self, args):
        # self.sequence = Sequence()
        # Define service here so that they can be alive throughout the runner's lifetime (scope issue)
        self.sequence = None
        self.logger = get_logger("Runner")
        self.args = args
        self.inspection_service = None
        self.grabber_service = None
        self.sequence = None

        self._initialize()
    
    def _select_grabber(self):
        if self.args.picamera:
            return PiCameraGrabberFactory.create()
        if self.args.camera:
            return CameraGrabberFactory.create()
        return FileGrabberFactory.create()

    def _select_sequence(self, inspection_service, grabber_service):
        if self.args.testseq:
            return TestSequence(inspection_service=inspection_service, grabber_service=grabber_service)
        return Sequence(inspection_service=inspection_service, grabber_service=grabber_service)

    def _initialize(self):
        if app_state.controller:
                app_state.controller.update_result(text="Runner started. Initializing services...")
        self.inspection_service = InspectionFactory.create()
        self.grabber_service = self._select_grabber()
        self.sequence = self._select_sequence(inspection_service=self.inspection_service, grabber_service=self.grabber_service)
        if app_state.controller:
                app_state.controller.update_result(text="Services initialized. Starting main loop...")  
                      
    def run(self):
        try:
            # Initialize services
            if app_state.controller:
                app_state.controller.update_result(text="Runner started. Initializing services...")
            inspection_service = InspectionFactory.create()
            grabber_service = self._select_grabber()
            self.sequence = self._select_sequence(inspection_service=inspection_service, grabber_service=grabber_service)
            if app_state.controller:
                app_state.controller.update_result(text="Services initialized. Starting main loop...")
            # Repeatedly runs the sequence every configured seconds
            while True:
                try: 
                    self.logger.info("Starting sequence run...")
                    self.sequence.run()
                    self.logger.info("Sequence run completed. Sleeping for 30 seconds...")
                except Exception as e:
                    self.logger.error(f"Runner ran into error while executing sequence in the loop -> {e}")

                # Wait 30 seconds before next loop
                time.sleep(AppConfigAdapter().load_loop_delay())
        except Exception as e:
            if app_state.controller:
                error_text = f"Runner execution failed to run. Not sequence error. Probably failed to initialize. -> {str(e)}"
                app_state.controller.update_result(text=error_text)
            raise RunnerException("Runner execution failed to run. Not sequence error. Probably failed to initialize.", e)
        
    def run_once(self):
        try:
            try: 
                self.logger.info("Starting sequence run...")
                if self.sequence is None:
                    raise RunnerException("Runner sequence is not initialized.")
                self.sequence.run()
                self.logger.info("Sequence run completed.")
            except Exception as e:
                self.logger.error(f"Runner ran into error while executing sequence in the loop -> {e}")
        except Exception as e:
            if app_state.controller:
                error_text = f"Runner execution failed to run. Not sequence error. Probably failed to initialize. -> {str(e)}"
                app_state.controller.update_result(text=error_text)
            raise RunnerException("Runner execution failed to run. Not sequence error. Probably failed to initialize.", e)
        finally:
            self.logger.info("Sequence run completed. Sleeping for configured seconds...")


if __name__ == "__main__":
    # runner = Runner()
    # runner.run()
    pass
