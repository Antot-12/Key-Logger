import unittest
from unittest.mock import patch
from pynput.keyboard import Key, KeyCode
from keylogger import Keylogger, get_current_language


class TestKeylogger(unittest.TestCase):

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_handle_basic_key(self, mock_lang):
        kl = Keylogger()

        kl.on_press(KeyCode.from_char('a'))
        self.assertEqual(kl.current_phrase, ['a'])

        kl.on_press(Key.space)
        self.assertEqual(kl.current_phrase, ['a', ' '])

        kl.on_press(KeyCode.from_char('b'))
        self.assertEqual(kl.current_phrase, ['a', ' ', 'b'])

        kl.on_press(Key.backspace)
        self.assertEqual(kl.current_phrase, ['a', ' '])  # Backspace should remove the last 'b'

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_handle_shift_and_special_chars(self, mock_lang):
        kl = Keylogger()

        kl.shift_pressed = True  # Simulate holding down shift
        kl.on_press(KeyCode.from_char('1'))  # Shift+1 should give '!'
        self.assertEqual(kl.current_phrase, ['!'])

        kl.on_release(Key.shift)  # Simulate releasing shift
        self.assertFalse(kl.shift_pressed)  # Shift should no longer be pressed

    @patch('keylogger.get_current_language', return_value=0x422)  # Ukrainian layout
    def test_ukrainian_layout(self, mock_lang):
        kl = Keylogger()

        kl.on_press(KeyCode.from_char('ф'))  # Ukrainian 'ф'
        self.assertEqual(kl.current_phrase, ['ф'])

        kl.on_press(KeyCode.from_char('і'))  # Ukrainian 'і'
        self.assertEqual(kl.current_phrase, ['ф', 'і'])

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_english_layout(self, mock_lang):
        kl = Keylogger()

        kl.on_press(KeyCode.from_char('a'))  # English 'a'
        self.assertEqual(kl.current_phrase, ['a'])

        kl.on_press(KeyCode.from_char('.'))  # English '.'
        self.assertEqual(kl.current_phrase, ['a', '.'])

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_phrase_completion(self, mock_lang):
        kl = Keylogger()

        kl.on_press(KeyCode.from_char('h'))
        kl.on_press(KeyCode.from_char('i'))
        kl.on_press(Key.enter)

        kl.finish_phrase()  # Simulate finishing a phrase

        self.assertEqual(kl.current_phrase, [])  # Phrase buffer should be cleared

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_special_chars_with_shift(self, mock_lang):
        kl = Keylogger()

        kl.shift_pressed = True  # Simulate holding down shift
        kl.on_press(KeyCode.from_char('2'))  # Shift+2 should give '@'
        self.assertEqual(kl.current_phrase, ['@'])

        kl.on_release(Key.shift)
        self.assertFalse(kl.shift_pressed)  # Shift should be released

    @patch('keylogger.get_current_language', return_value=0x422)  # Ukrainian layout
    def test_switching_language(self, mock_lang):
        kl = Keylogger()

        # Ukrainian input
        kl.on_press(KeyCode.from_char('ф'))  # Ukrainian 'ф'
        self.assertEqual(kl.current_phrase, ['ф'])

        # Simulate language change
        mock_lang.return_value = 0x409  # Switch to English

        kl.on_press(KeyCode.from_char('a'))  # English 'a'
        self.assertEqual(kl.current_phrase, ['ф', 'a'])  # Mixed input from different layouts

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_check_stop_combination(self, mock_lang):
        kl = Keylogger()

        # Simulate pressing Ctrl + Shift + q
        kl.on_press(Key.ctrl_l)
        kl.on_press(Key.shift)
        kl.on_press(KeyCode.from_char('q'))

        # Check if stop combination is detected
        self.assertTrue(kl.check_stop_combination())

        kl.on_release(Key.ctrl_l)
        kl.on_release(Key.shift)
        self.assertFalse(kl.check_stop_combination())  # After release, it should no longer work

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_handle_backspace(self, mock_lang):
        kl = Keylogger()

        kl.on_press(KeyCode.from_char('a'))
        kl.on_press(KeyCode.from_char('b'))
        kl.on_press(Key.backspace)  # Backspace should remove 'b'

        self.assertEqual(kl.current_phrase, ['a'])

        kl.on_press(Key.backspace)  # Another backspace should remove 'a'
        self.assertEqual(kl.current_phrase, [])

    @patch('keylogger.get_current_language', return_value=0x409)  # English layout
    def test_ignore_special_keys(self, mock_lang):
        kl = Keylogger()

        # Натискаємо спеціальні клавіші
        kl.on_press(Key.ctrl_l)
        kl.on_press(Key.alt_l)
        kl.on_press(Key.tab)

        # Спеціальні клавіші не повинні бути додані в current_phrase, окрім ctrl (для зупинки)
        self.assertEqual(kl.current_phrase, ['ctrl'])

        kl.on_release(Key.ctrl_l)
        self.assertEqual(kl.current_phrase, [])  # After releasing Ctrl, it should be empty

    def test_get_current_language(self):
        # Test that get_current_language returns a valid language code
        lang = get_current_language()
        self.assertIn(lang, [0x409, 0x422])  # Expect either 'en' or 'uk'


if __name__ == '__main__':
    unittest.main()
