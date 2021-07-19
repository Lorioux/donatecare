import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.urandom(128)
    
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default='')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', default='')
    MAIL_SUPPRESS_SEND = False


    SQLALCHEMY_BINDS = {
        "booking": "sqlite:///databases/booking.db",
        "profiles": "sqlite:///databases/profiles.db",
        "schedules": "sqlite:///databases/schedules.db",
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_REFRESH_EACH_REQUEST = True

    SESSION_COOKIE_NAME = "donatecare"

    JSONIFY_PRETTYPRINT_REGULAR = True
    # SERVER_NAME = "backend.localhost"


class TestingConfig(Config):

    SECRET_KEY = "ncamcajdansdkasaiskdaslfaljfoanjoakpmsdpadnaojfoamfanfo"

    ENV = "development"

    TESTING = True

    DEBUG = True

    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True

    SESSION_REFRESH_EACH_REQUEST = True

    SESSION_COOKIE_NAME = "donatecare"

    JSONIFY_PRETTYPRINT_REGULAR = True
    # SERVER_NAME = "backend.localhost"


class ProductionConfig(Config):
    SQLALCHEMY_BINDS = {
        "booking": "sqlite:///databases/booking.db", # set postsql
        "profiles": "sqlite:///databases/profiles.db", # set postsql
        "schedules": "sqlite:///databases/schedules.db", # set postsql
    }
    ENV = "production"
    DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR = True