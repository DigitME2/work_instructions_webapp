import logging
import sys

from flask import Flask
from sqlalchemy import create_engine

from app.default.models import User
from app.extensions import db, login_manager
from app.init_db import init_db

try:
    from config import Config
except ModuleNotFoundError:
    logging.error("Could not find config.py file. An example file is provided in example-confs")
    sys.exit()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
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

    @app.before_first_request
    def initial_setup():
        with app.app_context():
            init_db()

    return app
