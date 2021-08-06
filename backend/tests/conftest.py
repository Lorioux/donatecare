from __future__ import absolute_import
import json
# import subprocess as subpro
import os
from flask.helpers import url_for
# from flask.wrappers import Response



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
    # app.config["TESTING"] = True
    yield app
    session.remove()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# @pytest.fixture
@pytest.fixture(scope='session')
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
        specialities=speciality,
        addresses=address,
        licences=license,
        mode="video",
        birthdate="2000-02-01",
    )
    yield doctor


@pytest.fixture
def address():
    return [dict(
        streetname="Av. Carolina Michaelis",
        doornumber="49 RC-ESQ",
        zipcode="2795-050",
        state="Lisbon",
        city="Lisbon",
        country="Portugal",
    )]


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
            issuedate="20/02/2018",
            enddate="20/02/23",
            issuingorg="Ordem dos Medicos de Portugal",
            issuingcountry="Portugal",
            certificate="/media/profiles/licenses/certificate.pdf",
        ),
        dict(
            code="XMSNDCDHSJASK",
            issuedate="20/02/2020",
            enddate="20/02/25",
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
        addresses=address,
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
def schedules(processor):
    schedules = [
        dict(
            # doctorId=processor.get_publicid(),
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
    subscriber = [ dict(
        username="+351930400399",
        password="sacadcadffadadadadas",
        role="doctor",
        dob="2012/03/26",
        phone="+351930400399",
        fullname="John Doe",
        country="Portugal",
        gender="Male",
    ),
    dict(
        username="+351930400391",
        password="sacadcadffadadadadas",
        role="beneficiary",
        dob="2012/03/26",
        phone="+351930400391",
        fullname="Charley de Melo",
        country="Portugal",
        gender="Female",
    )]
    yield subscriber



class AuthActions(object):
    def __init__(self, client) -> None:
        self.client = client 

    def create(self, user):
        url = url_for("auth.create_credencials")
        return self.client.post(url, data=json.dumps(user), \
            content_type="application/josn", \
                follow_redirects=True
        )

    def authenticate(self, user):
        url = url_for("auth.authenticate")
        return self.client.post(url, data=json.dumps(user), \
            content_type="application/josn", \
                follow_redirects=True
        )

    def deauthenticate(self):
        url = url_for("auth.deauthenticate")
        return self.client.get(url, 
                follow_redirects=True)


@pytest.fixture
def credentials(client):
    actions = AuthActions(client)
    yield actions




class ResponseProcessor(object):
    
    

    def __init__(self) -> None:
        super().__init__()
        self.public_id = ''
    
    # @app.after_request
    def set_publicid(self, id):
        os.environ['PUBLIC_ID'] = id
    
    def get_publicid(self):
        return os.getenv("PUBLIC_ID", '')
        # return self.public_id
        
@pytest.fixture
def processor():
    processor = ResponseProcessor()
    yield processor
