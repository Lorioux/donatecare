
SQLALCHEMY_BINDS = {
    "booking": "sqlite:///databases/booking.db",
    "profiles": "sqlite:///databases/profiles.db",
    "schedules": "sqlite:///databases/schedules.db",
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "ncamcajdansdkasaiskdaslfaljfoanjoakpmsdpadnaojfoamfanfo"

ENV="development"

DEBUG = True

SESSION_REFRESH_EACH_REQUEST = True

SESSION_COOKIE_NAME = "donatecare"

JSONIFY_PRETTYPRINT_REGULAR = True
# SERVER_NAME = "backend.localhost"