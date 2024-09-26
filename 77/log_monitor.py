import time
import os
import shutil
from datetime import datetime
from config import config


def monitor_log_changes():
    log_dir = config.get('log_directory', 'logs')
    log_file_name = config.get('log_file', 'app.log')
    log_file = os.path.join(log_dir, log_file_name)

    if not os.path.exists(log_file):
        print(f"Log file '{log_file}' does not exist.")
        return

    last_modified_time = os.path.getmtime(log_file)
    last_size = os.path.getsize(log_file)
    monitoring_interval = config.get('monitoring_interval', 1)  # Check interval in seconds
    max_file_size = config.get('max_log_size', 5 * 1024 * 1024)  # Max size in bytes (default: 5MB)

    print(f"Monitoring changes for log file: {log_file}")

    # Optional timeout to stop monitoring after a certain period (e.g., 1 hour)
    timeout = config.get('monitoring_timeout', None)  # In seconds, None for no timeout
    start_time = time.time()

    while True:
        try:
            # Break after timeout period (if configured)
            if timeout and (time.time() - start_time) >= timeout:
                print(f"Monitoring timed out after {timeout} seconds.")
                break

            # Check if log file size or modification time changed
            current_modified_time = os.path.getmtime(log_file)
            current_size = os.path.getsize(log_file)

            if current_modified_time != last_modified_time or current_size != last_size:
                print(f"Log file '{log_file}' updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                # Display new log entries
                display_new_entries(log_file, last_size)

                # Automatically back up the log file
                backup_log_file(log_file)

                last_modified_time = current_modified_time
                last_size = current_size

            # Check file size and alert if it exceeds max size
            if current_size > max_file_size:
                print(f"Warning: Log file '{log_file}' exceeds max size of {max_file_size / (1024 * 1024)} MB!")

            time.sleep(monitoring_interval)

        except KeyboardInterrupt:
            print("Log monitoring stopped by user.")
            break
        except FileNotFoundError:
            print(f"Log file '{log_file}' was deleted or moved.")
            break


def display_new_entries(log_file, last_size):
    """Display new entries added to the log file since the last check."""
    with open(log_file, 'r') as f:
        f.seek(last_size)  # Start reading from the previous size
        new_lines = f.readlines()
        if new_lines:
            print("New log entries:")
            for line in new_lines:
                print(line.strip())
        else:
            print("No new log entries.")


def backup_log_file(log_file):
    """Create a timestamped backup of the log file in the same directory."""
    backup_dir = os.path.join(os.path.dirname(log_file), 'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f"{os.path.basename(log_file)}_{timestamp}.bak")
    shutil.copy2(log_file, backup_file)
    print(f"Backup created: {backup_file}")


def clear_log_file(log_file):
    """Clear the contents of the log file."""
    with open(log_file, 'w'):
        pass  # Open the file in write mode to empty its contents
    print(f"Log file '{log_file}' has been cleared.")


def stop_monitoring():
    """Stop the monitoring process manually."""
    print("Manual stop initiated.")
    exit()


if __name__ == "__main__":
    monitor_log_changes()
