import sys 
sys.path.append("..")


from flask import json

# from registration.models import Doctor, Speciality
from .conftest import delete_tables

def test_add_doctor(client, doctor):

    res = client.post("/members/subscribe", data=json.dumps(doctor), 
                        content_type="application/json", follow_redirects=True)
    id  = res.get_json()['id']
    # time.sleep(15)
    #delete_tables(doctor)
    assert None != id
    
def test_add_beneficiary(client, beneficiary):
    res = client.post("/members/subscribe", data=json.dumps(beneficiary), 
                        content_type="application/json", follow_redirects=True)
    id = res.get_json()['id']
    assert None != id