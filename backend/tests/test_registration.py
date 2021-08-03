from __future__ import absolute_import

from flask import json
from flask.helpers import url_for
import pytest

# from registration.models import Doctor, Speciality
# from backend.tests.conftest import delete_tables

@pytest.mark.run(order=5)
def test_add_practitioner(client, doctor):
    url = url_for("profiles.create_practitioner_profile")
    rv = client.post(
        "/members/createProfile",
        data=json.dumps(doctor),
        content_type="application/json",
        follow_redirects=True,
    )

    assert "successful" in str(rv.data)

@pytest.mark.run(order=10)
def test_add_beneficiary(client, beneficiary):
    rv = client.post(
        "/members/createProfile",
        data=json.dumps(beneficiary),
        content_type="application/json",
        follow_redirects=True,
    )
    id = rv.get_json()["id"]
    assert None != id


@pytest.mark.run(order=6)
def test_list_licences_by_practitioner(client, license):
    url = url_for("profiles.licences", doctorid=1)
    rv = client.get(url, follow_redirects=True)

    assert license[0]["code"] in str(rv.data)


@pytest.mark.run(order=7)
def test_find_doctors(client):
    criteria = [
        "speciality",
        "speciality-localtion",
        "speciality-localtion-mode",
        "mode",
        "all",
    ]

    for c in criteria:
        url = url_for("profiles.find_doctors", criteria=c)
        if c == "speciality":
            rv = client.get(
                url, # f"/members/doctors?",
                data=json.dumps({"speciality": "Nutritionist"}),
                content_type="application/json",
                follow_redirects=True,
            )
            # print(rv.data)
            assert "speciality" in str(rv.data)

        if c == "speciality-location":
            rv = client.get(
                url, # f"/members/doctors?criteria={c}",
                data=json.dumps({"speciality": "Nutritionist", "location": "Lisbon"}),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "mode":
            rv = client.get(
                url, # f"/members/doctors?criteria={c}",
                data=json.dumps({"mode": "video"}),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "speciality-location-mode":
            rv = client.get(
                url, # f"/members/doctors?criteria={c}",
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
            rv = client.get(
                    url,# f"/members/doctors?criteria={c}", 
                    follow_redirects=True)
            assert "speciality" in str(rv.data)

@pytest.mark.run(order=8)
def test_list_specialities(client):
    url = url_for("profiles.specialities")
    rv = client.get(
        url, # "/members/allSpecialities", 
        follow_redirects=True)
    assert "title" in str(rv.data)

    url = url_for("profiles.specialities", title="Nutritionist")
    rv = client.get(
            url, # "/members/findSpeciality?title=Nutritionist", 
                follow_redirects=True)
    assert "title" in str(rv.data)
