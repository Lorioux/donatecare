SQLALCHEMY_BINDS = {
    "booking": "sqlite:///booking/instance_file/booking.db",
    "profiles": "sqlite:///registration/instance_files/profiles.db",
    "schedules": "sqlite:///scheduling/instance_files/schedules.db",
}

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET = "ncamcajdansdkasaiskdaslfaljfoanjoakpmsdpadnaojfoamfanfo"


ENV="development"

SESSION_REFRESH_EACH_REQUEST = True

# SERVER_NAME = "backend.localhost"