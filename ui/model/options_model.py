from PySide6.QtCore import QObject, Signal
from adapters.config.app_config_handler import AppConfigHandler
class OptionsModel(QObject):
    options_changed = Signal(dict)  # emitted whenever options update

    def __init__(self, initial_options=None):
        super().__init__()
        self.pre_processed_options = AppConfigHandler.get_preprocess_options()
        self.post_processed_options = AppConfigHandler.get_postprocess_options()

    def get_preprocess_options(self):
        return self.pre_processed_options
    
    def get_postprocess_options(self):
        return self.post_processed_options

    def update_preprocess_option(self, key, value):
        """Change one setting and notify listeners."""
        if key in self.pre_processed_options:
            self.pre_processed_options[key] = value
            self.options_changed.emit(self.get_preprocess_options())

    def update_postprocess_option(self, key, value):
        """Change one setting and notify listeners."""
        if key in self.post_processed_options:
            self.post_processed_options[key] = value
            self.options_changed.emit(self.get_postprocess_options())

    def set_preprocess_options(self, new_dict):
        """Replace entire dictionary and notify."""
        self.pre_processed_options.update(new_dict)
        self.options_changed.emit(self.get_preprocess_options())

    def set_postprocess_options(self, new_dict):
        """Replace entire dictionary and notify."""
        self.post_processed_options.update(new_dict)
        self.options_changed.emit(self.get_postprocess_options())
