from __future__ import absolute_import


from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import and_

import pytest
from sqlalchemy.orm.session import Session, sessionmaker
from backend import (
    Beneficiary, 
    Doctor, 
    Speciality, 
    DoctorSpeciality,
    dbase
)

from backend.app import app

# session = Session(bind="__all__", expire_on_commit=False, autocommit=True)

@pytest.fixture(scope="session")
def client():
    with app.app_context():
        app.config["TESTING"] = True
        dbase.init_app(app)
        # dbase.create_all()
        yield app.test_client()

@pytest.fixture()
def doctor(speciality, address, license):
    doctor = dict(
            role = "doctor",
            name = "Dr. John Doe", 
            gender = "MALE",
            nif="XSDSDSMM4x", 
            phone="351920400949",
            photo="/media/profiles/doctors/foto.png",
            speciality=speciality,
            address=address,
            license = license,
            mode = "video call"         
    )
    yield doctor

@pytest.fixture
def address():
    return dict(
                road = "Av. Carolina Michaelis",
                flat = "49 RC-ESQ",
                zipcode = "2795-050",
                state = "Lisbon",
                city="Lisbon", 
                country="Portugal"
            )

@pytest.fixture
def speciality():
    speciality = [ 
        dict(
            title = "Nutritionist",
            details = '''
            Help people to adopt better eating habit for an enhanced lifestyle
            '''
        ),
        dict(
            title = "Dentist",
            details = "Help people to improve their dental hygiene"
        )]
    yield speciality

@pytest.fixture
def license():
    license = [
        dict(
            code="XMSNDUASLKDASK", 
            issue_date = "20/02/2018", 
            valid_date = "20/02/23", 
            issuer = "Ordem dos Medicos de Portugal", 
            country = "Portugal", 
            certificate = "/media/profiles/licenses/certificate.pdf",
        ),

        dict(
            code="XMSNDCDHSJASK", 
            issue_date = "20/02/2020", 
            valid_date = "20/02/25", 
            issuer = "Ordem dos Medicos de Portugal", 
            country = "Portugal", 
            certificate = "/media/profiles/licenses/certificate.pdf",
        )
    ]

    yield license

@pytest.fixture()
def beneficiary(address):
    beneficiary = dict(
        role="beneficiary",
        name= "Magido",
        age= 34,
        gender = "MALE",
        photo = "/media/profiles/beneficiaries/foto.jpg",
        phone="351920450673",
        nif="CSDXDCNSAMMX",
        address=address
    )

    yield beneficiary

# @app.teardown_appcontext
def delete_tables(
        doctor=None,
        beneficiary=None
    ):
    if doctor:
        Doctor.query.filter(and_(
            Doctor.name == doctor["name"],  
            Doctor.nif == doctor["nif"],
            Doctor.phone == doctor["phone"]
        )).delete()  

    if beneficiary:
        Doctor.query.filter(and_(
            Doctor.name == doctor["name"],  
            Doctor.nif == doctor["nif"],
            Doctor.phone == doctor["phone"]
        )).delete()
    # dbase.drop_all()
    dbase.session.commit()
    pass