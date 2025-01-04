from flask_mail import Message, Mail
from app.config import SingletonMeta


class NotificationService(metaclass=SingletonMeta):
    def __init__(self, mail: Mail):
        self.mail = mail

    def send_email(self, recipient: str, subject: str, body: str):
        try:
            msg = Message(subject, recipients=[recipient], body=body)
            self.mail.send(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False