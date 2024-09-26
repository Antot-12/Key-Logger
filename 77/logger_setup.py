# import os
# import shutil
# from logging.handlers import RotatingFileHandler
#
# from flask import logging
#
# from config import config
#
#
# def setup_logging(config):  # Explicitly accept config as a parameter
#     """Set up the logging configuration using the provided config dictionary."""
#     # Ensure that 'log_directory' and 'log_file' exist in the config
#     if 'log_directory' not in config or 'log_file' not in config:
#         raise ValueError("Config must contain 'log_directory' and 'log_file' fields.")
#
#     log_dir = config['log_directory']
#
#     # Create the log directory if it does not exist
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#
#     log_file = os.path.join(log_dir, config['log_file'])
#
#     # Set up the logger with the desired log file and format
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#
#     # Define the rotating file handler (log rotation at 5MB with up to 5 backups)
#     handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
#
#     # Define the log format
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#
#     # Add the handler to the logger
#     logger.addHandler(handler)
#
#     # Optionally log to console if specified in config
#     if config.get('log_to_console', False):
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         logger.addHandler(console_handler)
#
#     print(f"Logging set up. Writing logs to: {log_file}")
#
#
# def backup_logs():
#     """Back up log files to a 'backup' folder within the log directory."""
#     log_dir = config.get('log_directory')
#
#     if not os.path.exists(log_dir):
#         raise ValueError(f"Log directory '{log_dir}' does not exist.")
#
#     backup_dir = os.path.join(log_dir, 'backup')
#
#     # Create backup directory if it doesn't exist
#     if not os.path.exists(backup_dir):
#         os.makedirs(backup_dir)
#
#     # Generate a timestamped backup folder
#     from datetime import datetime
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     backup_subdir = os.path.join(backup_dir, f"backup_{timestamp}")
#     os.makedirs(backup_subdir)
#
#     # Copy all log files to the backup directory
#     for file_name in os.listdir(log_dir):
#         if file_name.endswith(".log"):
#             source_file = os.path.join(log_dir, file_name)
#             destination_file = os.path.join(backup_subdir, file_name)
#             shutil.copy2(source_file, destination_file)
#
#     print(f"Backup completed successfully to {backup_subdir}")
#


import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(config):
    """Set up logging using the provided config dictionary."""
    if 'log_directory' not in config or 'log_file' not in config:
        raise ValueError("Config must contain 'log_directory' and 'log_file' fields.")

    log_dir = config['log_directory']

    # Create the log directory if it does not exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, config['log_file'])

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add file handler
    logger.addHandler(handler)

    # Optionally log to console
    if config.get('log_to_console', False):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    print(f"Logging set up. Writing logs to: {log_file}")
