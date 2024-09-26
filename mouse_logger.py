from pynput import mouse
from datetime import datetime
from logger import Logger
from config import config

class MouseLogger:
    def __init__(self):
        self.logger = Logger()
        self.start_time = datetime.now().strftime(config.get('time_format', '%Y-%m-%d %H:%M:%S'))

    def start(self):
        """Запуск логування миші."""
        with mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        """Логування кліків миші."""
        current_time = datetime.now().strftime(config.get('time_format', '%Y-%m-%d %H:%M:%S'))
        if pressed:
            self.logger.log_event("mouse_click", {
                "button": str(button),
                "position": {"x": x, "y": y},
                "action": "pressed",
                "time": current_time
            }, level="INFO")
        else:
            self.logger.log_event("mouse_click", {
                "button": str(button),
                "position": {"x": x, "y": y},
                "action": "released",
                "time": current_time
            }, level="INFO")

    def on_scroll(self, x, y, dx, dy):
        """Логування скролінгу миші."""
        current_time = datetime.now().strftime(config.get('time_format', '%Y-%m-%d %H:%M:%S'))
        self.logger.log_event("mouse_scroll", {
            "position": {"x": x, "y": y},
            "scroll": {"dx": dx, "dy": dy},
            "time": current_time
        }, level="INFO")
