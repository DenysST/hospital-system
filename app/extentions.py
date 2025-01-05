from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import google.generativeai as genai
import os

db = SQLAlchemy()
migrate = Migrate()

