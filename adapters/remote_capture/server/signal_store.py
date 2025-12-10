from utils.logger import get_logger

class SignalStore:
    def __init__(self):
        self._signals = {}
        self.logger = get_logger()

    def set_signals(self, signals: dict):
        self.logger.debug(f"[DEBUG] set_signals called: {signals}")
        """Store full dict from master."""
        self._signals.update(signals) 

    def get_signals(self):
        """Return dict for slaves."""
        self.logger.debug(f"[DEBUG] SignalStore current state: {self._signals}")
        return self._signals
    
    def reset_signal(self, slave_id):
        """Reset only the specified slave's signal."""
        if slave_id in self._signals:
            self._signals[slave_id] = False
            self.logger.debug(f"[DEBUG] Reset {slave_id} → False")
        else:
            self.logger.debug(f"[DEBUG] reset_signal ignored — {slave_id} not in signals")
signal_store = SignalStore()
