from __future__ import absolute_import
import json

from flask import url_for
import pytest

@pytest.mark.run(order=3)
def test_signup(client, subscriber):
    url = url_for("auth.create_credencials")
    rv = client.post(
        url,
        data=json.dumps(subscriber),
        content_type="application/json",
        follow_redirects=True,
    )

    assert "success" in str(rv.data)



@pytest.mark.run(order=4)
def test_login(client, subscriber):
    url = url_for("auth.authenticate")
    rv = client.post(
        url,
        data=json.dumps(
            {
                "role": subscriber["role"],
                "userid": subscriber["username"],
                "password": subscriber["password"],
            }
        ),
        content_type="application/json",
        follow_redirects=True,
    )
    assert "success" in str(rv.data)


@pytest.mark.run(order=11)
def test_logout(client):
    url = url_for("auth.deauthenticate")
    rv = client.post(
        url,
        follow_redirects=True
    )

    assert "success" in str(rv.data)