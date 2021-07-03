import sys
sys.path.append("..")

from operator import and_
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import true


from backend.databases import dbase

class Beneficiaries(dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "beneficiaries"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(55))
    age = Column(Integer)
    phone = Column(String(55))
    nif = Column(String(55), unique=True)
    address = Column(String(128))
    city = Column(String(55))
    country = Column(String(55))

    def __init__(self, fullname, age, phone, nif):
        self.fullname = fullname
        self.age = age
        self.phone = phone
        self.nif = nif

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()

    def validate(self, fullname, phone, nif):
        valid = self.query.filter(and_(self.fullname.like(fullname), self.phone.like(phone), self.nif.like(nif))).first()
        if valid:
            return valid
        return None

class Doctors (dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "doctors"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    doctor_name = Column(String(55), unique=True)
    doctor_specs = dbase.relationship("Specialities", lazy="select", backref=backref('doctor', lazy='joined'))
    doctor_phone = Column(String(12), unique=True)
    doctor_nif = Column(String(55), unique=True)
    doctor_photo = Column(String(128))
    doctor_address = Column(String(128), unique=True)
    consultation_mode = Column(String(128))
    city = Column(String(55))
    country = Column(String(55))

    def __init__(self, doctor_name, doctor_phone, doctor_nif, doctor_photo, doctor_address):
        self.doctor_name = doctor_name
        self.doctor_phone = doctor_phone
        self.doctor_nif = doctor_nif
        self.doctor_photo = doctor_photo
        self.doctor_address = doctor_address

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()

class Specialities(dbase.Model):
    __tablename__ = "specialities"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(55), unique=True, nullable=False)
    detalhes = Column(Text)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="cascade"))

    def __init__(self, name, details, doctor_id):
        self.name = name 
        self.details = details
        self.doctor_id = doctor_id

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()

    def getby_name(self, name):
        return Specialities.query.filter(self.name.like(name))

class Licenses(dbase.Model):
    __tablename__ = "licenses"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    code =  Column(String(128), unique=True) # Encrypted
    issue_date = Column(String(8))
    due_date = Column(String(8))
    issuer = Column(String(128))
    country = Column(String(55))
    license = Column(String(128)) # Image path Encrypted
    doct_id = Column(Integer, ForeignKey("doctors.id"))


    def __init__(self, code, issue_date, due_date, issuer, country, license, id ):
        self.code = code
        self.issue_date = issue_date
        self.due_date = due_date
        self.issuer = issuer
        self.country = country
        self.license = license
        self.doct_id = id


    def save(self):
        dbase.session.add(self)
        dbase.session.commit()

    def getby_doctid(self, id):
        return self.query.filter(self.doct_id==id)