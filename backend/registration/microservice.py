from __future__ import absolute_import

from datetime import datetime
import uuid

from flask import Blueprint, json, request, jsonify
from flask.helpers import make_response, url_for
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from flasgger import swag_from

from backend.registration.models import (
    Beneficiary,
    Doctor,
    Address,
    License,
    Speciality,
)

from backend.authentication import token_required
from backend import Subscriber

profiles = Blueprint(
    "profiles",
    __name__,
    static_url_path="/media/uploads/",
    static_folder="media/uploads",
    url_prefix="/v1",
)


@profiles.route("/", methods=["GET"])
def subscribers():
    return jsonify({"response":"Not Implemented"})


@profiles.route("/practitioners", methods=["GET"])
@profiles.route("/practitioners/findByCriteria?criteria=<string:criteria>", methods=["GET"])
def find_doctors():
    request_time = datetime.now()
    try:

        data = request.get_json()
        criteria = request.args["criteria"]

        print(criteria, " : ", data)
        # find by speciality and location together
        if criteria == "speciality-location":
            doctors = Doctor().find_all(
                criteria=criteria, title=data["speciality"], city=data["location"]
            )

        if criteria == "speciality":
            doctors = Doctor().find_all(criteria=criteria, title=data["speciality"])

        if criteria == "speciality-location-mode":
            doctors = Doctor().find_all(
                criteria=criteria,
                speciality=data["speciality"],
                city=data["location"],
                mode=data["mode"],
            )

        if criteria == "mode":
            doctors = Doctor().find_all(criteria=criteria, mode=data["mode"])

        if criteria == "all":
            doctors = Doctor().find_all(criteria=criteria)

    except RuntimeError as error:
        print(error)
        return None
    print(doctors)

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
                street_name=addr.street_name,
                door_number=addr.door_num,
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
                "fullname": doctor.full_name,
                "identity": doctor.nif,
                "speciality": specialities,
                "licenses": licenses,
                "address": address,
                "mode": doctor.mode,
            }
        )
    template["metadata"]["responseTime"] = datetime.now()

    return jsonify(template)


@token_required
def create_profile(current_user: Subscriber = None, data: dict=None):
    
    if data is None:
        data = request.get_json()
    
    role = data["role"]

    if role in ["doctor", "beneficiary", "caregiver"]:
        result = handle_subscriptions(role, data)

        if result is not None:
            phone = data["phone"]

            return redirect(
                url_for(
                    "auth.add_authentication_keys",
                    data=json.dumps(
                        {
                            "private_key": result.nif,
                            "public_key": uuid.uuid3(
                                uuid.NAMESPACE_URL, f"{phone}-{role}"
                            ),
                        }
                    ),
                ),
                code=307,
            )

            # return jsonify({"id": result.id})
        return make_response(
            "Profile not created", 403, {"response": "Provide valid data"}
        )

    return make_response({"Error":"Too many errors", "message":"Check your inputs"}), 403


def handle_subscriptions(role, data):
    if role == "doctor":
        return add_practitioner(data=data)
    if role == "beneficiary":
        return add_beneficiary(data=data)
    return None


@token_required
def add_practitioner(current_user: Subscriber = None, data: dict = None):
    # address_id = add_member_address(data['address'])
    # if address_id is None:
    #     return None
    private_key = current_user.access_keys

    
    doctor = Doctor(
        fullname=data["fullname"],
        taxid=generate_password_hash(data["taxid"], method="SHA256"),
        phone=generate_password_hash(data["phone"], method="SHA256"),
        # photo=data["photo"],
        gender=data["gender"],
        mode=data["mode"],
        birthdate=data["birthdate"],
    )

    entity = doctor.check_uniqueness(data["phone"], data["taxid"])

    if entity:
        return entity 


    if doctor.save() is None:
        return make_response({"Error": "Failed to add practitioner"}), 403

    # handle specialities addition
    if not add_speciality(doctor, data.get("specialities")):
        doctor.delete()
        return make_response({"Error": "Failed to add specialities"}), 403

    if not add_license(doctor, data.get("licences")):
        doctor.delete()
        return make_response({"Error": "Failed to add licences"}), 403

    if not add_residence(doctor, data.get("addresses")):
        doctor.delete()
        return make_response({"Error": "Failed to add addresses"}), 403
    
    return doctor


@token_required
def add_beneficiary(current_user: Subscriber = None, data=dict()):
    
    beneficiary = Beneficiary(
        fullname=data["fullname"],
        birthdate=data["birthdate"],
        phone=generate_password_hash(data["phone"], method="SHA256"),
        gender=data["gender"],
        taxid=generate_password_hash(data["taxid"], method="SHA256"),
        address=data["address"],
    ).save()

    if beneficiary is None:
        return make_response({"Error": "Failed to add beneficiary"}), 403

    if not add_residence(beneficiary, data.get("addresses")):
        return make_response({"Error": "Failed to add addresses"}), 403
    return beneficiary


@profiles.route("/beneficiaries", methods=["GET"])
@token_required
def find_beneficiaries(current_user: Subscriber = None, *args, **kwargs):
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


@profiles.route("/updateMemberAddress")
@token_required
def add_member_address(current_user: Subscriber = None, data=dict()):
    address_id = Address(
        road=data["road"],
        flat=data["flat"],
        zipcode=data["zipcode"],
        state=data["state"],
        city=data["city"],
        country=data["country"],
    ).save()
    return address_id


@profiles.route("/licenses/<int:doctorid>", methods=["GET"])
@profiles.route("/doctor/<int:doctorid>/licences")
@token_required
def licences(current_user: Subscriber = None, doctorid=None):
    request_time = datetime.now()
    licenses = Doctor.query.get(doctorid).licenses
    print(licenses)
    if licenses is None or licenses == []:
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
                end_date=license.end_date,
                issuingorg=license.issuingorg,
                issuingcountry=license.issuingcountry,
                certificate=license.certificate,
            )
        )
    response = make_response(jsonify(template))
    response.set_cookie(key="OneTimeCookie", value="SMADNKASDNAKSNDAK", max_age=1800)
    return response


@profiles.route("/allSpecicialities", methods=["GET"])
@profiles.route("/findSpeciality?title=<string:title>", methods=["GET"])
@token_required
def specialities(current_user: Subscriber = None, title=None):
    request_time = datetime.now()
    specs = None

    if title is None:
        specs = Speciality().getby_title(title)
    else:
        specs = Speciality().get_all()

    template = {
        "metadata": {
            "requestTime": request_time,
            "domain": "practitioners",
            "responseTime": datetime.now(),
            "requestType": "specialities",
            "responses": len(specialities),
        },
        "summary": [],
    }

    if specialities is None:
        return jsonify({"response": "empty"})

    for speciality in specs:
        template["summary"].append(
            dict(title=speciality.title, details=speciality.details)
        )

    response_time = datetime.now()
    template["metadata"]["responseTime"] = response_time
    return jsonify(template)


@profiles.route('/updateSpeciality', methods=['POST', 'PUT'])
@token_required
def handle_speciality_update(current_user: Subscriber=None, content: dict = None):
    # validate content
    if content and "title" in content and "description" in content:
        pass


@profiles.route("/practitioner/createProfile", methods=["POST", "PUT"])
# @token_required
def create_practitioner_profile(current_user: Subscriber=None):

    profile : dict = request.get_json()
    role = "practitioner"

    # validate the request
    if validate_profile_entries(profile, role):

        for addr in profile.get("addresses"):
            validkeys, check = validate_address_entries(addr)
            if not check:
                return make_response({"Error" : "Wrong address keys",
                    "Valid keys" : validkeys
                    }), 403
        
        for specialiy in profile.get("specialities"):
            validkeys, check = validate_speciality_entries(specialiy)
            if not check:
                return make_response({"Error" : "Wrong speciality keys",
                    "Valid keys" : validkeys
                    }), 403
        
        for license in profile.get("licences"):
            validkeys, check = validate_license_entries(license)
            if not check:
                return make_response({"Error" : "Wrong license keys",
                    "Valid keys" : validkeys
                    }), 403
    
    return create_profile(data=profile)    


@profiles.route("/beneficiary/createProfile")
@token_required
def create_beneficiary_profile(current_user: Subscriber=None):
    
    profile : dict = request.get_json()
    role = "beneficiary"
    
    # validate the request
    if validate_profile_entries(profile, role):
        validkeys, check = validate_address_entries(profile.get("address"))
        if not check:
             return make_response({"Error" : "Wrong address keys",
                "Valid keys" : validkeys
                }), 403
    
    return create_profile(data=profile)    


def add_speciality(practitioner: Doctor, specialities: list):
    for spec in specialities:
        speciality = Speciality(title=spec.get("title"), description=spec.get("description")) \
            .save_with_practitioner(practitioner)
        if speciality is None:
            return False
    return True


def add_license(practitioner: Doctor, licences: list):
    for lic in licences:
        license = License(
            code=lic.get("code"),
            enddate=lic.get("enddate"),
            issuedate=lic.get("issuedate"),
            issuingcountry=lic.get("issuingcountry"),
            issuingorg=lic.get("issuingorg"),
            certificate=lic.get("certificate")
        ).save_with_licensee(practitioner)
        if license is None:
            return False
    return True


def add_residence(resindent:any, addresses: list):
    for addr in addresses:
        address = Address(
            city=addr.get("city"),
            country= addr.get("country"),
            doornumber=addr.get("doornumber"),
            zipcode=addr.get("zipcode"),
            state=addr.get("state"),
            streetname=addr.get("streetname")
        ).save_with_resident(resindent)
        if address is None:
            return False 
    return True


def validate_address_entries(address: dict):
    keys = {
        "city",
        "country",
        "doornumber",
        "zipcode",
        "state",
        "streetname"
    }
    #print(list(address.keys()))
    return list(keys), set(address.keys()).difference(keys) == {}

def validate_speciality_entries(speciality: dict):
    keys = {"description",
        "title"}
    
    return keys, set(speciality.keys()).difference(keys) == {}


def validate_license_entries(license: dict):
    keys = {
        "code",
        "enddate",
        "issuedate",
        "issuingcountry",
        "issuingorg",
        "certificate"
    }
    return list(keys), set(license.keys()).difference(keys) == {}

# def validate_mode_entry(mode)

def validate_profile_entries(profile_entry: dict, role: str):
    if role == "practitioner":
        keys = {
            "addresses",
            "birthdate",
            "licences",
            "fullname",
            "phone",
            "role",
            "specialities",
            "taxid",
            "mode",
            "gender"
        }
    keys = {
        "addresses",
        "birthdate",
        "fullname",
        "phone",
        "role",
        "taxid",
        "gender"
    }
    return list(keys), set(profile_entry.keys()).difference(keys) == {}