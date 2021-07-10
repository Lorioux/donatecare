from flask import Flask
from werkzeug.utils import redirect

import sys
sys.path.append("..")


app = Flask(__name__)

app.config.from_pyfile("config.py")


from backend.databases import initialize_dbase
from backend.registration import members
from backend.booking import bookings
from backend.scheduling import schedules

with app.app_context():
    initialize_dbase(app)

app.register_blueprint(members)
app.register_blueprint(bookings)
app.register_blueprint(schedules)


@app.route("/")
def index():
    return redirect("/booking")


if __name__ == "__main__":
    app.run("127.0.0.1", port=8000,debug=True)
