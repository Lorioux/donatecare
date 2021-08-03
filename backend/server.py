#!/bin/bash python

from __future__ import absolute_import


import sys
from waitress import serve


from app import make_app
from settings import ProductionConfig
import logging
from logging.handlers import RotatingFileHandler

from flask import request

log = logging.getLogger("werkzeug")
logging.basicConfig(
    level=logging.INFO,
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = RotatingFileHandler("./.logs/app.log", maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.Logger("werkzeug", logging.DEBUG)

app = make_app(ProductionConfig, handler)

@app.before_first_request
def setup_logging():
    if app.debug:
        log.addHandler(logging.StreamHandler(stream=sys.stdout))
    else:
        log.addHandler(handler)
@app.after_request
def log_request(response):
    
    app.logger.log(logging.DEBUG, msg="REQ: {} {} {}".format(request.method, request.path, response.status_code))
    # app.logger.log(logging.DEBUG, msg="REQ: {} {} {}".format(request.method, request.path, response.status))
    return response

serve(app, port=8080)