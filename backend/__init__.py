from flask import Flask
from flask.cli import with_appcontext
from werkzeug.utils import redirect

import sys
sys.path.append("..")


app = Flask(__name__)

app.config.from_pyfile('config.py')


from backend.databases import initialize_dbase
from backend.registration import regs
from backend.booking import bookings
from backend.scheduling import scheds

with app.app_context():
    initialize_dbase(app)

app.register_blueprint(regs)
app.register_blueprint(bookings)
app.register_blueprint(scheds)

@app.route("/")
def index():
    return redirect("/booking")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)