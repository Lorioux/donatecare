from __future__ import absolute_import

import logging
import sys, os
sys.path.append("..")


from flask import Flask, jsonify, json
from flasgger import Swagger

from backend import initialize_dbase, dbase, settings
from backend.registration.microservice import profiles
from backend.booking.microservice import bookings
from backend.scheduling.microservice import schedules
from backend.authentication.microservice import auth



def api_configurations(app: Flask, template):
    pass

def make_app(environment=None, log_handler=None):
    app = Flask(__name__, instance_relative_config=True)

    if environment:
        app.config.from_object(environment)
    else:
        app.config.from_object(settings.DevelopmentConfig)

    # app.run("0.0.0.0", port=8080, debug=True, load_dotenv=False)
    try:
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
    except OSError as error:
        logging.exception(error, stack_info=True)

    with open("./swagger/openapi.json") as file:
        template = json.loads(file.read())
        file.close()

    app.config["SWAGGER"] = {"title": "DONATE CARE", "uiversion": 3, "openapi": "3.0.1", "basePath":"/v1"}

    swagger = Swagger(app, template=template)

    # print(swagger.template['servers'][0]['variables'])


    dbase.init_app(app)

    with app.app_context():
        initialize_dbase(app)
        app.register_blueprint(profiles)
        app.register_blueprint(bookings)
        app.register_blueprint(schedules)
        app.register_blueprint(auth)
    
    
    @app.route("/")
    def index():
        app.logger.info(request.full_path)
        return jsonify({"status" : "ok", "apiversion":"1.0.0"})

    return app


if __name__ == "__main__":
    make_app()
