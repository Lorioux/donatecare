from __future__ import absolute_import
from flask.signals import appcontext_tearing_down


from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import and_

import pytest
from backend import Beneficiary, Doctor, Speciality, DoctorSpeciality, dbase, session

from backend.app import app
from backend import settings

# session = Session(bind="__all__", expire_on_commit=False, autocommit=True)


@pytest.fixture(scope="session")
def client():
    with app.app_context():
        app.config.from_object(settings.TestingConfig)

        dbase.init_app(app)
        dbase.create_all()
        print(app.config["SQLALCHEMY_BINDS"])
        yield app.test_client()


@pytest.fixture()
def doctor(speciality, address, license):
    doctor = dict(
        role="doctor",
        name="Dr. John Doe",
        gender="MALE",
        nif="XSDSDSMM4x",
        phone="351920400949",
        photo="/media/profiles/doctors/foto.png",
        speciality=speciality,
        address=address,
        license=license,
        mode="video call",
    )
    yield doctor


@pytest.fixture
def address():
    return dict(
        road="Av. Carolina Michaelis",
        flat="49 RC-ESQ",
        zipcode="2795-050",
        state="Lisbon",
        city="Lisbon",
        country="Portugal",
    )


@pytest.fixture
def speciality():
    speciality = [
        dict(
            title="Nutritionist",
            details="""
            Help people to adopt better eating habit for an enhanced lifestyle
            """,
        ),
        dict(title="Dentist", details="Help people to improve their dental hygiene"),
    ]
    yield speciality


@pytest.fixture
def license():
    license = [
        dict(
            code="XMSNDUASLKDASK",
            issue_date="20/02/2018",
            valid_date="20/02/23",
            issuer="Ordem dos Medicos de Portugal",
            country="Portugal",
            certificate="/media/profiles/licenses/certificate.pdf",
        ),
        dict(
            code="XMSNDCDHSJASK",
            issue_date="20/02/2020",
            valid_date="20/02/25",
            issuer="Ordem dos Medicos de Portugal",
            country="Portugal",
            certificate="/media/profiles/licenses/certificate.pdf",
        ),
    ]

    yield license


@pytest.fixture()
def beneficiary(address):
    beneficiary = dict(
        role="beneficiary",
        name="Magido",
        age=34,
        gender="MALE",
        photo="/media/profiles/beneficiaries/foto.jpg",
        phone="351920450673",
        nif="CSDXDCNSAMMX",
        address=address,
    )

    yield beneficiary


# @app.teardown_appcontext
def delete_tables(doctor=None, beneficiary=None):
    if doctor:
        Doctor.query.filter(
            and_(
                Doctor.name == doctor["name"],
                Doctor.nif == doctor["nif"],
                Doctor.phone == doctor["phone"],
            )
        ).delete()

    if beneficiary:
        Doctor.query.filter(
            and_(
                Doctor.name == doctor["name"],
                Doctor.nif == doctor["nif"],
                Doctor.phone == doctor["phone"],
            )
        ).delete()
    # dbase.drop_all()
    dbase.session.commit()
    pass


# Scheduling configurations
@pytest.fixture
def schedules():
    schedules = [
        dict(
            doctorId="XSDSDSMM4x",
            year=2021,
            month="aug",
            weeks={
                "3": dict(
                    days=["mon", "tue", "wed", "sat"],
                    timeslots=[
                        ["12:00", "13:00", "15:00"],
                        ["14:00", "16:00"],
                        ["8:00", "10:00", "15:00"],
                        ["10:00", "13:00", "16:00", "18:00"],
                    ],
                )
            },
        )
    ]
    yield schedules


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
