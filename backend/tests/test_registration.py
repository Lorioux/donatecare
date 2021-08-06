from __future__ import absolute_import

from flask import json
from flask.helpers import url_for
import pytest

# from registration.models import Doctor, Speciality
# from backend.tests.conftest import delete_tables
public_id = None


@pytest.mark.run(order=5)
def test_add_practitioner(client, doctor):
    url = url_for("profiles.create_practitioner_profile")
    rv = client.post(
        url,
        data=json.dumps(doctor),
        content_type="application/json",
        follow_redirects=True,
    )

    assert "successful" in str(rv.data)


@pytest.mark.run(order=6)
def test_find_practitioners(client, app, processor):
    
    criteria = [
        "speciality-only",
        "localtion-only"
        "speciality-localtion",
        "speciality-localtion-mode",
        "mode-only",
        "none",
    ]

    for c in criteria:
        url = url_for("profiles.find_practtioners_by_criteria", criteria=c)
        if c == "speciality-only":
            rv = client.get(
                url, # f"/members/doctors?",
                data=json.dumps({"speciality": "Nutritionist"}),
                content_type="application/json",
                follow_redirects=True,
            )
            # print(rv.data)
            data = rv.get_json()
            processor.set_publicid(data.get('summary')[0].get('publicid'))
            assert "speciality" in str(rv.data)

        if c == "speciality-location":
            rv = client.get(
                url, # f"/members/doctors?criteria={c}",
                data=json.dumps({"speciality": "Nutritionist", "location": "Lisbon"}),
                content_type="application/json",
                follow_redirects=True,
            )
            assert "speciality" in str(rv.data)

        if c == "mode-only":
            rv = client.get(
                url, # f"/members/doctors?criteria={c}",
                data=json.dumps({"mode": "video"}),
                content_type="application/json",
                follow_redirects=True,
            )
            
            assert "speciality" in str(rv.data)

        if c == "location-only":
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

        if c == "none":
            rv = client.get(
                    url,# f"/members/doctors?criteria={c}", 
                    follow_redirects=True)
            
            assert "speciality" in str(rv.data)


@pytest.mark.run(order=7)
def test_list_licences_by_practitioner(client, license, processor):
    
    url = url_for("profiles.licences", publicid=processor.get_publicid())
    
    print(url)

    rv = client.get(url, follow_redirects=True)

    assert license[0]["code"] in str(rv.data)


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


@pytest.mark.run(order=13)
def test_remove_beneficiary_by_practitioner(client, beneficiary):
    '''TODO'''
    # url = url_for("profiles.disassociate_beneficiary", beneficiary)
    # rv = client.get(
    #         url,
    #         follow_redirects=True
    # )
    pass


@pytest.mark.run(order=12)
def test_add_beneficiary_by_practitioner(client, credentials, beneficiary):
    url = url_for("profiles.create_beneficiary_profile")
    rv = client.post(
        url,
        data=json.dumps(beneficiary),
        content_type="application/json",
        follow_redirects=True,
    )

    assert 'success' in str(rv.data)


# @app.after_request
#     def retrieve_publicid(response):
#         data = response.get_json()
#         if data is not None and "summary" in data.keys():
#             processor.set_publicid(data.get('summary')[0].get('publicid'))
#             print("CALLED...", processor.get_publicid())
#         print(data)