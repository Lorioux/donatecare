from flask.blueprints import Blueprint
from flask import request

from flask.json import jsonify




from .models import Beneficiaries

regs = Blueprint(__name__, __name__, static_url_path="/media/uploads/", 
    static_folder="media/uploads", url_prefix="/members")



@regs.route("/registries")
def subscribers():
    registeries = Beneficiaries.query.all()
    return jsonify({
        "Full name":  registeries[0].fullname,
        "Age": registeries[0].age,
        "Phone": registeries[0].phone,
        "NIF": registeries[0].nif
    })


@regs.route("/subsribe", methods=["POST"])
def subscribe():
    data = request.args.body
    role = data["role"]
    if role in ["doctor",  "beneficiary", "caregiver"]:
        handle_subscriptions(role, data)


def handle_subscriptions(role, data):
    if role == "doctor":
        doctor = data
