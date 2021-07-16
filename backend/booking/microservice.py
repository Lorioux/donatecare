from __future__ import absolute_import

from flask import Blueprint, request, jsonify
from flask.globals import current_app, g
from flask.helpers import url_for
from sqlalchemy.orm import query
from werkzeug.utils import redirect

from backend.booking.models import Appointment
from backend.registration.models import Beneficiary

bookings = Blueprint("booking", __name__, url_prefix="/booking")

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
    return redirect(url_for(".subscribe", method="GET"))


# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5001,debug=True)
