

from flask.blueprints import Blueprint
from flask.json import jsonify


scheds = Blueprint(__name__, __name__, url_prefix="/schedules")

@scheds.route("/all")
def get_all():
    return jsonify({""})

@scheds.route("/<date>", methods=["GET"])
def getby_date():
    return jsonify({""})

@scheds.route("/weeks/<number>/<year>")
def getby_week():
    return jsonify({""})