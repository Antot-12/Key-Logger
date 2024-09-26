import json
import os

config = {}  # Global variable for the config dictionary

def create_default_config():
    """Create default config if config.json does not exist."""
    default_config = {
        "log_directory": "logs",
        "log_file": "app.log",
        "backup_interval": 3600,
        "session_duration": 3600,
        "delay_between_records": 1,
        "log_time": True,
        "time_format": "%Y-%m-%d %H:%M:%S",
        "log_special_keys": True,
        "log_key_combinations": True,
        "log_to_console": True,
        "screenshot_on_log": False,
        "screen_capture_directory": "screenshots",
        "analysis_directory": "analysis",
        "data_analysis": True,
        "interactive_mode": False,
        "application_filter": [],
        "resource_monitoring": False,
        "mouse_logging": False,
        "db_logging": False,
        "db_type": "sqlite",
        "db_path": "app.db",
        "db_table": "logs",
        "web_interface": False,
        "external_api_integration": False,
        "api_endpoints": [],
        "toggle_key": "ctrl+alt",
        "monitoring_interval": 2,
        "max_log_size": 10485760,
        "monitoring_timeout": 3600,
        "exclude_keys": []
    }

    # Create config.json if it doesn't exist
    with open('config.json', 'w') as config_file:
        json.dump(default_config, config_file, indent=4)
    print("Created config.json with default parameters.")

def load_config():
    """Load the configuration from config.json."""
    global config  # Refer to the global variable
    config_file = 'config.json'

    # Check if config.json exists, otherwise create it
    if not os.path.exists(config_file):
        print("config.json not found. Creating a new one with default values.")
        create_default_config()

    # Load the config.json file into the global config variable
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            print("Loaded config:", config)  # Debug: Show the loaded config
    except json.JSONDecodeError as e:
        print(f"Error loading config.json: {e}")
        raise

    # Ensure log_directory and log_file exist in the config
    if 'log_directory' not in config or 'log_file' not in config:
        raise ValueError("Config must contain 'log_directory' and 'log_file' fields.")
