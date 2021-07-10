from backend.tests.conftest import address
import sys

from sqlalchemy.orm.session import Session 
sys.path.append("..")


from flask.blueprints import Blueprint
from flask import request

from flask.json import jsonify
from backend.databases import dbase

from .models import Beneficiary, Country, Doctor, MemberAddress, Speciality

members = Blueprint(
    "members",
    __name__,
    static_url_path="/media/uploads/",
    static_folder="media/uploads",
    url_prefix="/members",
)


@members.route("/profiles", methods=["GET"])
def subscribers():
    role = request.path
    print(role)
    beneficiary = Beneficiary.query.all()
    return jsonify(
        {
            "Full name": beneficiary[0].fullname,
            "Age": beneficiary[0].age,
            "Phone": beneficiary[0].phone,
            "NIF": beneficiary[0].nif,
        }
    )


@members.route("/doctors", methods=["GET"])
def find_doctors():
    doctors = Doctor.query.all()
    template = []
    for doctor in doctors:
        template += {
            "name" : doctor.name,
            "identity": doctor.nif,
            "speciality": Speciality.getby_id(id=doctor.id),
            "address" : doctor.address,
            "mode" : doctor.mode,
        }
    return jsonify(template)


@members.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    
    role = data["role"]
    
    if role in ["doctor", "beneficiary", "caregiver"]:
        result = handle_subscriptions(role, data)
        
        if result is not None:
            return jsonify({"id": result})
        else:
            return jsonify({"id": None})


def handle_subscriptions(role, data):
    if role == "doctor":
        return add_doctor(data=data)
    if role == "beneficiary":
        return add_beneficiary(data=data)
    return None 

def add_doctor(data):
    address_id = add_member_address(data["address"])
    if address_id is None:
        return None
    doctor_id = Doctor(
            name = data["name"], 
            nif = data["nif"], 
            phone = data["phone"],
            photo = data["photo"], address=address_id, 
            mode = data["mode"]).save()

    if doctor_id is not None:
        speciality_id = 0
        for name in data["speciality"]:
            speciality = Speciality(name, "BlaBla", doctor_id)
            speciality_id =  speciality.save()
        if speciality_id is None:
            return None
        
    return doctor_id

def add_beneficiary(data):
    address_id = add_member_address(data["address"])
    if address_id is None:
        return None
    beneficiary_id = Beneficiary(
                name=data["name"], 
                age = data["age"], 
                phone = data["phone"], 
                nif = data["nif"], address=address_id).save()
    return beneficiary_id

def add_member_address(data):
    country_id = Country(name=data["country"]).find_by("name")
    
    if country_id is None:
        return None
    data["country"] = country_id
    address_id = MemberAddress(
        road = data["road"], 
        flat=data["flat"], 
        zipcode=data["zipcode"], 
        city=data["city"], 
        country=data["country"]).save()
    return address_id