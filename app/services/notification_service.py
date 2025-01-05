from flask_mail import Message, Mail


class NotificationService:
    def __init__(self, mail: Mail):
        self._mail = mail

    def send_email(self, recipient: str, subject: str, body: str):
        try:
            msg = Message(subject, recipients=[recipient], body=body)
            self._mail.send(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False