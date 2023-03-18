import os

basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.abspath(os.path.join(basedir, os.pardir))


class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DEBUG = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(parentdir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1 hour


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test-db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
