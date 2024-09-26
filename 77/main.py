from api_integration import on_external_api_event
from config import load_config, config  # Import the config dictionary from the config module
from gui import show_gui
from logger_setup import setup_logging
from web_interface import show_web_interface
from database import setup_database_logging
from log_monitor import monitor_log_changes


def start_logging():
    load_config()  # Load the configuration into the global config dictionary
    print(f"Config after loading: {config}")  # Debugging: Print the loaded config
    setup_logging(config)  # Pass the config dictionary explicitly to setup_logging
    if config.get('db_logging'):
        setup_database_logging()
    if config.get('interactive_mode'):
        show_gui()
    if config.get('video_recording'):
        pass
    if config.get('activity_detection'):
        monitor_log_changes()
    if config.get('web_interface'):
        show_web_interface()
    if config.get('external_api_integration'):
        on_external_api_event()

if __name__ == "__main__":
    start_logging()
