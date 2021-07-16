from __future__ import absolute_import

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask.helpers import make_response

from backend.registration.models import (
    Beneficiary, Country, Doctor, Address, License, Speciality )

membership = Blueprint(
    "members",
    __name__,
    static_url_path="/media/uploads/",
    static_folder="media/uploads",
    url_prefix="/members",
)


@membership.route("/profiles", methods=["GET"])
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


@membership.route("/doctors", methods=["GET"])
def find_doctors(*args, **kwargs):
    request_time = datetime.now()
    doctors = Doctor().find_all(criterion="speciality", name="Nutritionist")
    template = {
        "metadata": {
            "requestTime": request_time,
            "domain": "practitioners",
            "responseTime": datetime.now(),
            "speciality": "Nutritionist",
            "location": "all",
            "responses": doctors.count(),
        },
        "summary": [],
    }
    # print(doctors)
    for doctor in doctors:
        address = list(
            dict(
                road=addr.road,
                flat=addr.flat,
                zipcode=addr.zipcode,
                state=addr.state,
                city=addr.city,
                country=addr.country.name,
            )
            for addr in doctor.addresses
            if addr is not None or addr.city == "Lisbon"
        )
        # print(address)
        specialities = list(s.title for s in doctor.specialities[0:])
        # print(specialities)
        licenses = list(l.code for l in doctor.licenses[0:])
        # print(licenses)
        template["summary"].append(
            {
                "name": doctor.name,
                "identity": doctor.nif,
                "speciality": specialities,
                "licenses": licenses,
                "address": address,
                "mode": doctor.mode,
            }
        )
    template["metadata"]["responseTime"] = datetime.now()
    return jsonify(template)


@membership.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()

    role = data["role"]

    if role in ["doctor", "beneficiary", "caregiver"]:
        result = handle_subscriptions(role, data)

        if result is not None:
            return jsonify({"id": result.id})
        return jsonify({"id": None})

    return None

def handle_subscriptions(role, data):
    if role == "doctor":
        return add_doctor(data=data)
    if role == "beneficiary":
        return add_beneficiary(data=data)
    return None


@membership.route("/updateDoctorProfile", methods=["PUT"])
def add_doctor(data=dict()):
    # address_id = add_member_address(data['address'])
    # if address_id is None:
    #     return None
    doctor = Doctor(
        name=data["name"],
        nif=data["nif"],
        phone=data["phone"],
        photo=data["photo"],
        mode=data["mode"],
        address=data["address"],
        speciality=data["speciality"],
        license=data["license"],
    ).save()

    if doctor is None:
        return None

    return doctor


@membership.route("/updateBenefiaciaryProfile", methods=["PUT"])
def add_beneficiary(data=dict()):
    # address_id = add_member_address(data["address"])
    # if address_id is None:
    #     return None

    beneficiary = Beneficiary(
        name=data["name"],
        age=data["age"],
        phone=data["phone"],
        nif=data["nif"],
        address=data["address"],
    ).save()

    if beneficiary is None:
        return None

    return beneficiary


@membership.route("/beneficiaries", methods=["GET"])
def find_beneficiaries(*args, **kwargs):
    request_time = datetime.now()
    beneficiaries = Beneficiary().find_all(criterion="city", name="Lisbon")
    # if beneficiaries is None or beneficiaries == []:
    #     print(beneficiaries)
    #     return None
    template = {
        "metadata": {
            "requestTime": request_time,
            "responseTime": datetime.now(),
            "domain": "beneficiary",
            "location": "Lisbon",
            "responses": beneficiaries.count(),
        },
        "summary": [],
    }

    for beneficiary in beneficiaries.all():

        addresses = list(
            dict(
                road=address.road,
                flat=address.flat,
                zipcode=address.zipcode,
                city=address.city,
                country=address.country.name,
            )
            for address in beneficiary.addresses
            if address is not None and address.city == "Lisbon"
        )
        template["summary"].append(
            dict(
                id=beneficiary.id,
                name=beneficiary.name,
                age=beneficiary.age,
                gender=beneficiary.gender,
                photo=beneficiary.photo,
                phone=beneficiary.phone,
                nif=beneficiary.nif,
                addresses=addresses,
            )
        )
    template["metadata"]["responseTime"] = datetime.now()
    return jsonify(template)


@membership.route("/updateMemberAddress")
def add_member_address(data=dict()):
    # get or add the country
    # country_id = Country(name=data["country"]).find_by("name")

    # if country_id is None:
    #     return None
    # data["country"] = country_id
    address_id = Address(
        road=data["road"],
        flat=data["flat"],
        zipcode=data["zipcode"],
        state=data["state"],
        city=data["city"],
        country=data["country"],
    ).save()
    return address_id


@membership.route("/licenses/<int:docid>", methods=["GET"])
@membership.route("/doctor/<int:doctorid>/licences")
def licences(doctorid):
    request_time = datetime.now()
    licenses = Doctor.query.get(doctorid).licenses
    if licenses is None:
        return jsonify({"response": "empty"})
    template = {
        "metadata": {
            "requestTime": request_time,
            "domain": "practitioners",
            "responseTime": datetime.now(),
            "requestTyle": "licences",
            "responses": len(licenses),
        },
        "summary": [],
    }

    for license in licenses:
        template["summary"].append(
            dict(
                code=license.code,
                issue_date=license.issue_date,
                valid_date=license.valid_date,
                issuer=license.issuer,
                country=license.country,
                certificate=license.certificate,
            )
        )
    response = make_response(jsonify(template))
    response.set_cookie(key="OneTimeCookie", value="SMADNKASDNAKSNDAK", max_age=1800)
    return response
