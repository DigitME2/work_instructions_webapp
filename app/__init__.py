import sys
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


try:
    from config import Config
except ModuleNotFoundError:
    logging.error("Could not find config.py file. An example file is provided as config.py.example")
    sys.exit()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.default import bp as default_bp
    from app.login import bp as login_bp
    from app.part_creation import bp as part_creation_bp
    from app.prod_recording import bp as prod_recording_bp

    app.register_blueprint(default_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(part_creation_bp)
    app.register_blueprint(prod_recording_bp)

    return app
