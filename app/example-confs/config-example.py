import getpass
import os


class Config(object):

    # If the URI is provided directly, use that
    if os.environ.get('DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    else:

        DATABASE_USER = os.environ.get('DATABASE_USER') or "postgres"
        DATABASE_ADDRESS = os.environ.get('DATABASE_ADDRESS') or "localhost"
        DATABASE_PORT = os.environ.get('DATABASE_PORT') or "5432"
        DATABASE_NAME = os.environ.get('DATABASE_NAME') or "webapp"

        DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

        SQLALCHEMY_DATABASE_URI = "postgres://{user}:{password}@{address}:{port}/{database}".format(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            address=DATABASE_ADDRESS,
            port=DATABASE_PORT,
            database=DATABASE_NAME)

    # Sqlite uri, use for quick testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"

    SECRET_KEY = os.environ.get('SECRET_KEY') or "3chv8db8L3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.realpath('app/static/images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', '.png', '.jpg', '.jpeg', '.gif'}
