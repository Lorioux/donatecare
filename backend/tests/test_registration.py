from __future__ import absolute_import

from flask import json

# from registration.models import Doctor, Speciality
# from backend.tests.conftest import delete_tables


def test_00_add_doctor(client, doctor):

    rv = client.post(
        "/members/createProfile",
        data=json.dumps(doctor),
        content_type="application/json",
        follow_redirects=True,
    )
    print(rv)
    id = rv.get_json()["id"]
    # time.sleep(15)
    # delete_tables(doctor)
    assert None != id


def test_01_add_beneficiary(client, beneficiary):
    rv = client.post(
        "/members/createProfile",
        data=json.dumps(beneficiary),
        content_type="application/json",
        follow_redirects=True,
    )
    id = rv.get_json()["id"]
    assert None != id


def test_02_list_licences(client, license):
    rv = client.get("/members/doctor/1/licences", follow_redirects=True)

    assert license[0]["code"] in str(rv.data)


def test_03_find_doctors(client):
    criteria = [
        "speciality",
        "speciality-localtion",
        "speciality-localtion-mode",
        "mode",
        "all",
    ]

    for c in criteria:
        if c == "speciality":
            rv = client.get(
                f"/members/doctors?criteria={c}",
                data=json.dumps({"speciality": "Nutritionist"}),
                content_type="application/json",
                follow_redirects=True,
            )
            # print(rv.data)
            assert "speciality" in str(rv.data)

        if c == "speciality-location":
            rv = client.get(
                f"/members/doctors?criteria={c}",
                data=json.dumps({"speciality": "Nutritionist", "location": "Lisbon"}),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "mode":
            rv = client.get(
                f"/members/doctors?criteria={c}",
                data=json.dumps({"mode": "video"}),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "speciality-location-mode":
            rv = client.get(
                f"/members/doctors?criteria={c}",
                data=json.dumps(
                    {
                        "speciality": "Nutritionist",
                        "location": "Lisbon",
                        "mode": "video",
                    }
                ),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "all":
            rv = client.get(f"/members/doctors?criteria={c}", follow_redirects=True)
            assert "speciality" in str(rv.data)


def test_04_list_specialities(client):
    rv = client.get("/members/allSpecialities", follow_redirects=True)
    assert "title" in str(rv.data)

    rv = client.get("/members/findSpeciality?title=Nutritionist", follow_redirects=True)
    assert "title" in str(rv.data)
