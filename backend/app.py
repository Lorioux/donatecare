from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_pyfile("config.py")

from . import initialize_dbase, dbase

dbase.init_app(app)

with app.app_context():
    
    from .registration.microservice import membership
    from .booking.microservice import bookings
    from .scheduling.microservice import schedules
    initialize_dbase(app)
    app.register_blueprint(membership)
    app.register_blueprint(bookings)
    app.register_blueprint(schedules)

    
    # initialize_dbase()

# def create_app(testing=False):
    #     app.config.from_pyfile("config.py")
        
    #     from backend.databases import initialize_dbase
    #     initialize_dbase(app)
    #     from backend.registration import members
    #     from backend.booking import bookings
    #     from backend.scheduling import schedules

    #     app.register_blueprint(members)
    #     app.register_blueprint(bookings)
    #     app.register_blueprint(schedules)

    #     return app

    # app = create_app()

@app.route("/")
def index():
    return jsonify("Welcome")

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000,debug=True, load_dotenv=True)
        
        # initialize_dbase(app)
