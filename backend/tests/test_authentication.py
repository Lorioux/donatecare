from __future__ import absolute_import
import json

import pytest

@pytest.mark.run(order=3)
def test_practitioner_signup(credentials, subscriber):
    rv =  credentials.create(subscriber[0])

    assert "success" in str(rv.data)



@pytest.mark.run(order=4)
def test_practitioner_login(credentials, subscriber):
    user = {
            "role": subscriber[0]["role"],
            "userid": subscriber[0]["username"],
            "password": subscriber[0]["password"],
        }

    rv =  credentials.authenticate(user)

    assert "success" in str(rv.data)


@pytest.mark.run(order=20)
def test_logout(credentials):
    rv =  credentials.deauthenticate()

    assert "success" in str(rv.data)