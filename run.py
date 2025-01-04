from flask_mail import Mail
from app.services.notification_service import NotificationService
from app import create_app

app = create_app()
mail = Mail(app)
notification_service = NotificationService(mail)

if __name__ == "__main__":
    app.run()