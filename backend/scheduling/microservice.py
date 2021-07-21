from __future__ import absolute_import


from logging import Logger
from os import abort
from flask import Blueprint, json, jsonify, request
from flask.helpers import url_for
from sqlalchemy.sql.elements import and_
from werkzeug.utils import redirect

from backend.scheduling.models import Schedule

LOG = Logger("SCHEDULING")
schedules = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules.route("/createSchedule", methods=["POST"])
def create(schedule=None):
    # create a single
    if schedule is not None:
        res = Schedule(
            year=schedule["year"],
            weeks=schedule["weeks"],
            month=schedule["month"],
            doctor_nif=schedule["doctorId"],
        ).save()
        return res

    # create multiple
    data = json.loads(request.data)
    count = data.__len__()
    schedules = [
        Schedule(
            year=schedule["year"],
            weeks=schedule["weeks"],
            month=schedule["month"],
            doctor_nif=schedule["doctorId"],
        ).save()
        for schedule in data
        if schedule is not None
    ]

    if not None in schedules and len(schedules) == count:
        return jsonify("successfully")

    return abort()


@schedules.route("/updateSchedule", methods=["PUT"])
def update():
    data = json.loads(request.data)
    old = None
    for schedule in data:
        if schedule is not None:
            old = Schedule.query.filter(
                and_(
                    Schedule.month.like(schedule["month"]),
                    Schedule.year == schedule["year"],
                ),
                Schedule.doctor_nif == schedule["doctorId"],
            ).one_or_none()
            if old is None:
                redirect(url_for(".create", schedule=schedule))
            old.weeks.update(schedule["weeks"])

    print(old.weeks)
    return jsonify(old.weeks)


@schedules.errorhandler(401)
def create_error():
    return "Not Allowed"


@schedules.route("/all")
def get_all():
    return jsonify({""})


@schedules.route("/<date>", methods=["GET"])
def getby_date():
    return jsonify({""})


@schedules.route("/weeks/<number>/<year>")
def getby_week():
    return jsonify({""})
