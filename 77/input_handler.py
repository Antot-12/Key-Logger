from pynput import keyboard, mouse
import time

pressed_keys = set()  # Набір для відстеження натиснутих клавіш
recording = False  # Флаг для керування записом
last_record_time = time.time()  # Час останнього запису

def start_key_logging():
    # Старт прослуховування клавіатури
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def on_press(key):
    global pressed_keys, recording, last_record_time

    # Додаємо натиснуту клавішу до набору
    pressed_keys.add(key)

    if recording:
        current_time = time.time()
        if (current_time - last_record_time) >= 1:  # Затримка між записами
            try:
                key_char = key.char  # Якщо це звичайна клавіша
            except AttributeError:
                key_char = f'[{key}]'  # Якщо це спеціальна клавіша (Shift, Ctrl, тощо)

            print(f"Key pressed: {key_char}")
            last_record_time = current_time  # Оновлення часу запису

def on_release(key):
    global pressed_keys, recording

    # Видаляємо клавішу з набору, коли вона відпущена
    if key in pressed_keys:
        pressed_keys.remove(key)

    # Вихід з програми на клавішу Esc
    if key == keyboard.Key.esc:
        return False

    # Можливе перемикання режиму запису при певній комбінації клавіш
    if key == keyboard.Key.f12:  # Наприклад, клавіша F12 перемикає запис
        recording = not recording
        print(f"Запис {'увімкнено' if recording else 'вимкнено'}")

def start_mouse_logging():
    # Старт прослуховування подій миші
    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) by ({dx}, {dy})")

# Стартуємо логування клавіатури
if __name__ == "__main__":
    start_key_logging()
