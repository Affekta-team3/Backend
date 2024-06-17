from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views

try:
    app.logger.info("Database connected successfully.")
except Exception as e:
    app.logger.error(f"Database connection failed: {e}")
