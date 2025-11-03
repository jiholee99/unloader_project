from exceptions.exception import AppConfigException
import json

class AppConfigHandler:
    """Handles application configuration settings."""   
    def _load_config():
        try:
            config_path = "config/app_config.json"
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return config_data
        except Exception as e:
            raise AppConfigException("Failed to load configuration file.", e)
        
    @staticmethod
    def get_logger_options() -> dict:
        """Retrieve logger options from config.
        If not found, returns empty dict.
        Data structure:
        {
            "log_to_file": <bool>,
            "log_level": <str>,
            "log_file_path": <str>
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("logger_options", {})

    @staticmethod
    def get_preprocess_options() -> dict:
        """Retrieve preprocessing options from config.
        If not found, returns empty dict.
        Data structure:
        {
            "threshold": int,
            "max_threshold": int
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("preprocess_options", {})

    @staticmethod
    def get_postprocess_options() -> dict:
        """Retrieve postprocessing options from config.
        If not found, returns empty dict.
        Data structure:
        {
            "min_contour_area": int,
            "use_fill_holes": bool
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("postprocess_options", {})