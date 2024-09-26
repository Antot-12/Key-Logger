# 🔑 Keylogger & Sensitive Data Analyzer

🎯 **Keylogger & Sensitive Data Analyzer** is a tool designed to track and record key presses on your keyboard, helping to detect sensitive information such as **emails**, **passwords**, and **login credentials**. It logs inputs in real-time, analyzes the data for security breaches, and offers easy management of logs with useful features like stop key combinations and multi-language support. 🌐

## 🌟 Features

- 📝 **Key Press Tracking**: Efficiently logs all key presses, including special keys (like `Shift`, `Enter`, `Backspace`), with precise timestamps.
- 🔐 **Sensitive Data Detection**: Automatically scans logs for **emails**, **passwords**, and **logins**, allowing you to monitor sensitive information.
- 🌍 **Multi-Language Support**: Detects different keyboard layouts (e.g., English 🇺🇸, Ukrainian 🇺🇦) to handle multi-language inputs seamlessly.
- 🗂 **Log Organization**: Automatically organizes logs into timestamped files in the `logs/` folder, making it easy to track and review key events.
- ⏹ **Custom Stop Key Combination**: Define custom key combinations to securely stop the logger (e.g., `Ctrl + Shift + Q`).
- ⚙️ **Flexible Configuration**: Configure key logging behavior, including the detection of special keys, sending email alerts, and stopping the logger.
- 📧 **Email Integration**: Sends logs to your email address based on predefined settings in `config.json`.

## 📁 Project Structure

```bash
.
├── .venv/                         # Virtual environment directory
├── logs/                          # Contains log files
│   └── log_2024-09-27_01-34-04.txt # Example log file with timestamps
├── unittest/                      # Contains unit tests
│   ├── test_keylogger.py          # Unit tests for the keylogger
├── config.json                    # Configuration file
├── config.py                      # Configuration loader and handler
├── email_sender.py                # Sends logs via email
├── key_generator.py               # Key encryption utility
├── keylogger.py                   # Main keylogger functionality
├── logger.py                      # Handles logging of key events
├── main.py                        # Entry point to start the keylogger
├── mouse_logger.py                # Tracks mouse events
└── sensitive_analyzer.py          # Scans logs for sensitive data like emails or passwords
```

## 🚀 How It Works

1. **Logging Keys**: The keylogger captures key presses and logs them in real-time. Logs are saved in the `logs/` folder as timestamped `.txt` files.
2. **Sensitive Data Analysis**: The `sensitive_analyzer.py` script scans the logs to identify **emails**, **passwords**, and **logins** based on predefined patterns.
3. **Stop Key Combination**: The keylogger can be stopped by pressing a custom combination of keys (e.g., `Ctrl + Shift + Q`).

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/keylogger-sensitive-data-analyzer.git
   cd keylogger-sensitive-data-analyzer
   ```

2. **Install dependencies** using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**:
   - Modify the `config.json` file to set custom stop key combinations, email notifications, and other options.

### Example `requirements.txt`

Make sure you create a **`requirements.txt`** file in your project root folder:

```plaintext
pynput==1.7.6
cryptography==3.4.7
PyInstaller==4.5
```

This file lists the required Python packages for the keylogger to run.

## ▶️ Usage

1. **Run the Keylogger**:
   ```bash
   python main.py
   ```

2. **Analyze Logs** for Sensitive Data:
   ```bash
   python sensitive_analyzer.py
   ```

This command scans the logs for potential sensitive data, such as:
- **Emails**: Detected emails like `example@gmail.com`.
- **Passwords**: Strings matching common password patterns.
- **Logins**: Short strings often resembling usernames or login credentials.

### 💾 Example Log Entry:

Each log entry contains detailed information about the key press:

```json
{
  "timestamp": "2024-09-27 01:34:04",
  "level": "INFO",
  "event_type": "key_press",
  "details": {
    "key": "a"
  }
}
```

Logs are stored in files like `log_2024-09-27_01-34-04.txt` under the `logs/` folder. You can analyze these logs using the `sensitive_analyzer.py` tool.

## 🧪 Unit Testing

Unit tests are provided in the `unittest/` folder. To run the tests, use the following command:

```bash
python -m unittest discover unittest/
```

This command will automatically discover and run all unit tests, ensuring that the keylogger and sensitive data analyzer work correctly.

## 🔧 Configuration

You can customize the keylogger settings in the `config.json` file. Here are a few key options:

- **`log_special_keys`**: Set to `true` to log special keys (e.g., `Shift`, `Ctrl`).
- **`stop_combination`**: Define a custom key combination to stop the logger (e.g., `["Key.ctrl_l", "Key.shift", "q"]`).
- **`send_email`**: Set to `true` to enable email alerts with the logs.
- **`email_settings`**: Configure SMTP settings for sending email alerts.

### Example `config.json`:

```json
{
  "log_file": "keylog.txt",
  "log_special_keys": true,
  "stop_combination": ["Key.ctrl_l", "Key.shift", "q"],
  "send_email": true,
  "email_settings": {
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "email_from": "logger@example.com",
    "email_to": "recipient@example.com",
    "email_password": "yourpassword"
  }
}
```

## 📧 Email Notifications

If email notifications are enabled, logs will be sent to the configured email address. Customize your SMTP server settings in the `config.json` file for this feature to work.

## 🎯 Keylogger Flow

1. **Start the Keylogger**: Logs are automatically generated and saved in real-time.
2. **Track Key Presses**: Every keystroke is captured and stored with details such as timestamps and key type.
3. **Analyze Sensitive Data**: The analyzer scans logs for potential sensitive information.
4. **Stop the Keylogger**: You can stop the logger using a predefined key combination (e.g., `Ctrl + Shift + Q`).

