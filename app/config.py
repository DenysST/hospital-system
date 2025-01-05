import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/hospital_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "denys.stefanko@gmail.com"  # Replace with your email
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = "denys.stefanko@gmail.com"
