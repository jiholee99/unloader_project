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
    def get_roi_settings() -> dict:
        """Retrieve ROI settings from config.
        If not found, returns empty dict.
        Data structure:
        {
            "roller_roi": {
                "x": int,
                "y": int,
                "w": int,
                "h": int
            }
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("roi", {})

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
    
    @staticmethod
    def get_judgement_options() -> dict:
        """Retrieve judgment options from config.
        If not found, returns empty dict.
        Data structure:
        {
            "fullness_cutoff": float
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("judgement_options", {})
    
    @staticmethod
    def get_loop_delay_seconds() -> int:
        """Retrieve loop delay seconds from config.
        If not found, returns default of 30 seconds.
        Data structure:
        {
            "loop_delay_seconds": int
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("loop_delay_seconds", 30)
    
    @staticmethod
    def get_roller_close_task_options() -> dict:
        """Retrieve roller close task options from config.
        If not found, returns empty dict.
        Data structure:
        {
            "min_threshold" : 100,
            "max_threshold" : 255,
            "crop_roi" : {
                "x": 200,
                "y": 150,
                "w": 100,
                "h": 100
            },
            "use_remove_bright_line" : true
        }
        """
        config_data = AppConfigHandler._load_config()
        return config_data.get("roller_close_task_options", {})