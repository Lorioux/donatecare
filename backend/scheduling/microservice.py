from flask.blueprints import Blueprint
from flask.json import jsonify


schedules = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules.route("/all")
def get_all():
    return jsonify({""})


@schedules.route("/<date>", methods=["GET"])
def getby_date():
    return jsonify({""})


@schedules.route("/weeks/<number>/<year>")
def getby_week():
    return jsonify({""})
