
SQLALCHEMY_BINDS = {
    "booking": "sqlite:///databases/booking.db",
    "profiles": "sqlite:///databases/profiles.db",
    "schedules": "sqlite:///databases/schedules.db",
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET = "ncamcajdansdkasaiskdaslfaljfoanjoakpmsdpadnaojfoamfanfo"

ENV="development"

SESSION_REFRESH_EACH_REQUEST = True

# SERVER_NAME = "backend.localhost"