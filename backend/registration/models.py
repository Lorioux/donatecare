from os import name
import sys
sys.path.append("..")

from operator import and_
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship


from backend.databases import dbase

class Beneficiary(dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "beneficiary"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(55))
    age = Column(Integer)
    phone = Column(String(55))
    nif = Column(String(55), unique=True)
    address = Column(Integer, ForeignKey("address.id"), nullable=False)

    def __init__(self, name, age, phone, nif, address):
        self.name = name
        self.age = age
        self.phone = phone
        self.nif = nif
        self.address = address

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except:
            return None

    def validate(self, fullname, phone, nif):
        valid = self.query.filter(and_(self.name.like(fullname), self.phone.like(phone), self.nif.like(nif))).first()
        if valid:
            return valid
        return None

class Doctor (dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "doctor"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(55), unique=True)
    # speciality = relationship("Speciality", backref=backref("doctor", lazy="dynamic"))
    phone = Column(String(12), unique=True)
    nif = Column(String(55), unique=True)
    photo = Column(String(128), default="/media/profiles/doctors/foto.jpg")
    address = Column(Integer, ForeignKey("address.id"), nullable=False)
    mode = Column(String(55), default="present")

    def __init__(self, name, nif, phone,
                    photo, address, mode):
        self.name = name
        self.phone = phone
        self.nif = nif
        self.photo = photo
        self.address = address
        self.mode = mode

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except:
            return None

    def delete(self):
        dbase.session.delete(self)
        dbase.session.commit()

class Speciality(dbase.Model):
    __tablename__ = "speciality"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(55), unique=True, nullable=False)
    details = Column(Text(256))
    doctor_id = Column(Integer, ForeignKey("doctor.id", ondelete="CASCADE"))

    def __init__(self, name, details, doctor_id):
        self.name = name 
        self.details = details
        self.doctor_id = doctor_id

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except:
            return None

    def getby_name(self, name):
        return Speciality.query.filter(name.like(name))

    def __call__(self, *args: any, **kwds: any) -> any:
        return super().__call__(*args, **kwds)
    
    def getby_id(self, id):
        return Speciality.query.filter(id == id)

class License(dbase.Model):
    __tablename__ = "license"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    code =  Column(String(128), unique=True) # Encrypted
    issue_date = Column(String(8))
    due_date = Column(String(8))
    issuer = Column(String(128))
    country = Column(Integer, ForeignKey("country.id"))
    license = Column(String(128), default="/media/profiles/licences/foto.jpg") # Image path Encrypted
    doct_id = Column(Integer, ForeignKey("doctor.id"))


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

class Country(dbase.Model):
    __tablename__ = "country"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)

    def __init__(self, name: any):
        self.name = name


    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except RuntimeError as e:
            print("Error Country: ", e.args)
            dbase.session.rollback()
            return None

    def find_by(self, criterion: any):
        if criterion == "id":
            country = Country.query.filter(Country.id == self.id).first()
        else:
            country = Country.query.filter(Country.name.like(self.name)).first()
        
        if country is None:
            self.save()
            return self.id
             
        return country.id

class MemberAddress(dbase.Model):
    __tablename__ = "address"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    road = Column(String(128))
    flat = Column(String(55))
    zipcode  = Column(String(9))
    city = Column(String(55))
    country = Column(Integer, ForeignKey("country.id"))
    
    def __init__(self, road, flat, zipcode, city, country) -> None:
        self.road = road
        self.flat = flat
        self.zipcode = zipcode
        self.city = city 
        self.country = country

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except RuntimeError as e:
            print(e)
            dbase.session.rollback()
            return None
        