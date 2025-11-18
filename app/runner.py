import time
from app.sequence import Sequence
from tests.test_sequence import TestSequence
from adapters.config import AppConfigAdapter
from utils.logger import get_logger

class Runner:
    def __init__(self):
        # self.sequence = Sequence()
        self.sequence = TestSequence()
        self.logger = get_logger("Runner")
        
    def run(self):
        # Repeatedly runs the sequence every 30 seconds
        while True:
            try:
                self.logger.info("Starting sequence run...")
                self.sequence.run()
                self.logger.info("Sequence run completed. Sleeping for 30 seconds...")
            except Exception as e:
                self.logger.error(f"Runner encountered an error: {e}")

            # Wait 30 seconds before next loop
            time.sleep(AppConfigAdapter().load_loop_delay())


if __name__ == "__main__":
    runner = Runner()
    runner.run()
