from core.runner.sequence import Sequence

class Runner:
    def __init__(self):
        self.sequence = Sequence()
        
    def run(self):
        # Have to add loop logic where after run completes, will sleep 30 seconds and run again
        self.sequence.run()

if __name__ == "__main__":
    runner = Runner()
    runner.run()