from __future__ import absolute_import

from flask import Blueprint
from flask.globals import current_app, g
from flask.json import jsonify
from flask import request
from sqlalchemy.orm import query
from werkzeug.utils import redirect

import sys

sys.path.append("..")

bookings = Blueprint("booking", __name__, url_prefix="/booking")

from .models import Appointment
from ..registration.models import Beneficiary

@bookings.route("/")
def booking():
    appointment = Appointment.query.all()
    print(appointment)

    return jsonify(
        {
            "periodFrom": "01/20/2021",
            "periodTo": "30/06/2021",
            "specialities": {
                "nutrition": {
                    "02/05/2021": {
                        "appointments": {
                            "slot": {
                                "12:00": [
                                    {
                                        "doctor": "Dr. John Doe",
                                        "doctorId": "xascascascac",
                                        "beneficiary": "Jose Melo",
                                        "beneficiaryId": "cmnsnadsdap",
                                    }
                                ]
                            }
                        }
                    }
                },
                "pediatric": {},
            },
        }
    )


@bookings.route("/makeAppointment", methods=["POST", "GET"])
def make_appointment():
    data = {}

    # beneficiary = data['beneficiary']
    # check if beneficiary is already registered

    beneficiary = Beneficiary.query.all()

    if beneficiary:
        # register appointment
        # appointment = Appointment(
        #     date=data.date, slot=data.time,
        #     doctorName=data.doctor, doctSpeciality=data.speciality,
        #     beneficiaryName=data.myName, beneficiaryPhone=data.beneficiaryPhone,
        #     beneficiaryNIF=data.beneficiaryNIF )
        # dbase.session_add(Appointment)
        return jsonify({"query": beneficiary[0].fullname})
    else:
        redirect("/subscribe", data={"beneficiary": ""})
        pass


# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5001,debug=True)
