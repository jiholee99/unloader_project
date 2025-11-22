import time
from app.sequence import Sequence
from test.test_sequence import TestSequence
from adapters.config import AppConfigAdapter
from utils.logger import get_logger
from app.factory import InspectionFactory, CameraGrabberFactory
from exceptions.exception import RunnerException
class Runner:
    def __init__(self):
        # self.sequence = Sequence()
        # Define service here so that they can be alive throughout the runner's lifetime (scope issue)
        self.sequence = None
        self.logger = get_logger("Runner")
        
    def run(self):
        try:
            inspection_service = InspectionFactory.create()
            grabber_service = CameraGrabberFactory.create()
            self.sequence = TestSequence(inspection_service=inspection_service, grabber_service=grabber_service)
            # Repeatedly runs the sequence every 30 seconds
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
            raise RunnerException("Runner execution failed to run. Not sequence error. Probably failed to initialize.", e)


if __name__ == "__main__":
    runner = Runner()
    runner.run()
