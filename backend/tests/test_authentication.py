from __future__ import absolute_import
import json

from flask import session

def test_07_signup(client, subscriber):
    rv = client.post(
            "/authentication/createCredentials",
            data=json.dumps(subscriber), \
                content_type="application/json", \
                    follow_redirects=True)

    assert "successfully" in str(rv.data)

def test_08_login(client, subscriber):
    rv = client.post(
            "/authentication/login",
            data=json.dumps({
                "role": subscriber["role"],
                "userid": subscriber["username"],
                "password": subscriber["password"]
            }), \
                content_type="application/json", \
                    follow_redirects=True)
    assert "successfully" in str(rv.data)
