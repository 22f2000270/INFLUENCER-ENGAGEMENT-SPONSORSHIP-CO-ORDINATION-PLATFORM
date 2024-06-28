# application/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.config import LocalDevelopmentConfig
from application.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they do not exist

    return app
