from __future__ import absolute_import


import json


def test_06_add_schedules(client, schedules):
    rv = client.post(
        "/schedules/createSchedule",
        data=json.dumps(schedules),
        content_type="application/json",
        follow_redirects=True,
    )

    assert "successfully" in str(rv.data)


def test_07_update_schedules(client, schedules):
    schedules[0]["weeks"]["week31"]["timeslots"]["fri"] = ["08:00", "14:00"]
    schedules[0]["weeks"].update(
        {"week32": dict(timeslots={"mon": ["08:00", "14:00", "23:00"]})}
    )

    rv = client.put(
        "/schedules/updateSchedule",
        data=json.dumps(schedules),
        content_type="application/json",
        follow_redirects=True,
    )

    assert "23:00" in str(rv.data)
