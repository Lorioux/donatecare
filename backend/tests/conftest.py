from __future__ import absolute_import



# from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import and_

import pytest
from backend import dbase, session

from backend.app import make_app
from backend import settings

# session = Session(bind="__all__", expire_on_commit=False, autocommit=True)
@pytest.fixture(scope='session')
def app():
    app = make_app(settings.TestingConfig)
    yield app
    session.remove()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def client(app):
    with app.test_request_context():
                
        yield app.test_client()

        

@pytest.fixture()
def doctor(speciality, address, license):
    doctor = dict(
        role="doctor",
        fullname="Dr. John Doe",
        gender="MALE",
        taxid="XSDSDSMM4x",
        phone="351920400949",
        photo="/media/profiles/doctors/foto.png",
        speciality=speciality,
        address=address,
        license=license,
        mode="video",
        birthdate="2000-02-01",
    )
    yield doctor


@pytest.fixture
def address():
    return dict(
        streetname="Av. Carolina Michaelis",
        doornumber="49 RC-ESQ",
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
            description="""
            Help people to adopt better eating habit for an enhanced lifestyle
            """,
        ),
        dict(title="Dentist", description="Help people to improve their dental health"),
    ]
    yield speciality


@pytest.fixture
def license():
    license = [
        dict(
            code="XMSNDUASLKDASK",
            issue_date="20/02/2018",
            valid_date="20/02/23",
            issuingorg="Ordem dos Medicos de Portugal",
            issuingcountry="Portugal",
            certificate="/media/profiles/licenses/certificate.pdf",
        ),
        dict(
            code="XMSNDCDHSJASK",
            issue_date="20/02/2020",
            valid_date="20/02/25",
            issuingorg="Ordem dos Medicos de Portugal",
            issuingcountry="Portugal",
            certificate="/media/profiles/licenses/certificate.pdf",
        ),
    ]

    yield license


@pytest.fixture()
def beneficiary(address):
    beneficiary = dict(
        role="beneficiary",
        fullname="John Doe",
        birthdate="2000-01-02",
        gender="MALE",
        photo="/media/profiles/beneficiaries/foto.jpg",
        phone="351 920 450 673",
        taxid="CSDXDCNSAMMX",
        address=address,
    )

    yield beneficiary


# @app.teardown_appcontext
def delete_tables(doctor=None, beneficiary=None):
    if doctor:
        Doctor.query.filter(
            and_(
                Doctor.name == doctor["name"],
                Doctor.nif == doctor["taxid"],
                Doctor.phone == doctor["phone"],
            )
        ).delete()

    if beneficiary:
        Doctor.query.filter(
            and_(
                Doctor.name == doctor["name"],
                Doctor.nif == doctor["taxid"],
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
                "week31": dict(
                    timeslots={
                        "mon": ["12:00", "13:00", "15:00"],
                        "tue": ["14:00", "16:00"],
                        "wed": ["8:00", "10:00", "15:00"],
                        "sat": ["10:00", "13:00", "16:00", "18:00"],
                    }
                )
            },
        )
    ]
    yield schedules


@pytest.fixture
def subscriber():
    subscriber = dict(
        username="+351930400399",
        password="sacadcadffadadadadas",
        role="doctor",
        dob="2012/03/26",
        phone="+351930400399",
        fullname="John Doe",
        country="Portugal",
        gender="Male",
    )
    yield subscriber