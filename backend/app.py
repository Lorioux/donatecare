from __future__ import absolute_import

from flask import Flask, jsonify
from backend import initialize_dbase, dbase
from backend.registration.microservice import membership
from backend.booking.microservice import bookings
from backend.scheduling.microservice import schedules

app = Flask(__name__)
app.config.from_pyfile("settings.py")

dbase.init_app(app)

with app.app_context():
    initialize_dbase(app)
    app.register_blueprint(membership)
    app.register_blueprint(bookings)
    app.register_blueprint(schedules)


@app.route("/")
def index():
    return jsonify("Welcome")


if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True, load_dotenv=True)

    # initialize_dbase(app)
