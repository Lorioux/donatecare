from __future__ import absolute_import

from flask import json

# from registration.models import Doctor, Speciality
from backend.tests.conftest import delete_tables

# def test_add_doctor(client, doctor):

#     res = client.post("/members/subscribe", data=json.dumps(doctor),
#                         content_type="application/json", follow_redirects=True)
#     id  = res.get_json()['id']
#     # time.sleep(15)
#     #delete_tables(doctor)
#     assert None != id

# def test_add_beneficiary(client, beneficiary):
#     res = client.post("/members/subscribe", data=json.dumps(beneficiary),
#                         content_type="application/json", follow_redirects=True)
#     id = res.get_json()['id']
#     assert None != id

# def test_licences_listing(client, license):
#     res = client.get("/members/doctor/1/licences", content_type="application/json")

#     assert license[0]["code"] in res.get_json()["summary"][0]["code"]

def test_find_doctors(client):
    criteria = ["speciality", "speciality-localtion", "speciality-localtion-mode", "mode", "all" ]
    
    for c in criteria:
        if c == "speciality":
            rv = client.get(f"/members/doctors?criteria={c}", \
                    data=json.dumps({"speciality": "Nutritionist"}), \
                        content_type="application/json", follow_redirects=True)
            # print(rv.data)
            assert "speciality" in str(rv.data)

        if c == "speciality-location":
            rv = client.get(f"/members/doctors?criteria={c}", \
                    data=json.dumps({"speciality": "Nutritionist", \
                        "location":"Lisbon"}), \
                            content_type="application/json", follow_redirects=True)
            assert "speciality" in str(rv.data)

        if c == "mode":
            rv = client.get(f"/members/doctors?criteria={c}", \
                    data=json.dumps({"mode": "video"}), \
                        content_type="application/json", follow_redirects=True)
            assert "speciality" in str(rv.data)

        if c == "speciality-location-mode":
            rv = client.get(f"/members/doctors?criteria={c}", \
                    data=json.dumps({"speciality": "Nutritionist", \
                        "location":"Lisbon", "mode":"video"}), \
                            content_type="application/json", follow_redirects=True)
            assert "speciality" in str(rv.data)

        if c == "all":
            rv = client.get(f"/members/doctors?criteria={c}", follow_redirects=True)
            assert "speciality" in str(rv.data)
