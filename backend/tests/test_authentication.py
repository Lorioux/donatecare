from __future__ import absolute_import
import json

from flask import session

def test_07_signup(client, subscriber):
    rv = client.post(
        "/Authentication/createCredentials",
        data=json.dumps(subscriber), \
            content_type="application/json", \
                follow_redirects=True,
    )

    assert "successfully" in str(rv.data)
