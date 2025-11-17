from adapters.config.app_config_handler import AppConfigHandler

class AppConfigAdapter:
    def load_preprocess(self): return AppConfigHandler.get_preprocess_options()
    def load_postprocess(self): return AppConfigHandler.get_postprocess_options()
    def load_judgement(self): return AppConfigHandler.get_judgement_options()
    def load_loop_delay(self): return AppConfigHandler.get_loop_delay_seconds()
    def load_roi(self): 
        roi = AppConfigHandler.get_roi_settings()
        return [roi["x"], roi["y"], roi["w"], roi["h"]]
