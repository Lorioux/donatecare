from os import name
import sys
from sqlalchemy.orm.session import Session

from sqlalchemy.sql.expression import null

sys.path.append("..")

from operator import and_
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, relationship

from backend.databases import dbase, initializer

class Beneficiary(dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "beneficiary"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String(55))
    age = Column(Integer)
    phone = Column(String(55))
    nif = Column(String(55), unique=True)
    address_id = Column(Integer, ForeignKey("address.id", use_alter=True), nullable=False)
    addresses = relationship("MemberAddress", primaryjoin="Beneficiary.address_id==MemberAddress.id", foreign_keys=[address_id])

    def __init__(self, *args, **kwargs):        
        self.name = initializer("name", kwargs)
        self.age = initializer("age", kwargs)
        self.phone = initializer ("phone",kwargs)
        self.nif = initializer ("nif", kwargs)
        self.address = add_address(initializer ("address", kwargs))


    def __call__(self, *args: any, **kwds: any):
        return self

    def save(self):
        dbase.session.add(self)
        try:
            new_address = add_address(self.addresses)
            if new_address.save() is None:
                return None
            else:
                self.addresses.append(new_address)
            return self.id
        except:
            return None
    
    @staticmethod
    def add_address(address):
        return MemberAddress(address)

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
    
    phone = Column(String(12), unique=True)
    nif = Column(String(55), unique=True)
    photo = Column(String(128), default="/media/profiles/doctors/foto.jpg")
    mode = Column(String(55), default="present")

    speciality_id = Column(Integer, ForeignKey("speciality.id", use_alter=True))
    specialities = relationship("Speciality", foreign_keys=[speciality_id])

    license_id = Column(Integer, ForeignKey("license.id", ondelete="CASCADE", use_alter=True))
    licenses = relationship("License", foreign_keys=[license_id])

    address_id = Column(Integer, ForeignKey("address.id", ondelete="CASCADE", use_alter=True))
    addresses = relationship("MemberAddress", foreign_keys=[address_id])


    def __init__(self, **kwargs):
        self.name = initializer("name", kwargs)
        self.phone = initializer("phone", kwargs)
        self.nif = initializer("nif", kwargs)
        self.photo = initializer("photo", kwargs)
        self.address = initializer("address", kwargs)
        self.mode = initializer("mode", kwargs)
        self.speciality = initializer("speciality", kwargs)
        self.license = initializer("license", kwargs)

    def save(self):
        session = dbase.session
        session.begin()
        
        try:
            session.add(self)
            dbase.session.commit()
            if self.link_speciality(session=session, speciality=self.speciality) is None:
                return None

            elif self.link_licenses(session=session, licenses=self.license) is None:
                return None

            elif self.link_addresses(session=session, address=self.address) is None:
                return None

            else:
                return self.id
                
        except:
            return None

    def delete(self):
        dbase.session.delete(self)
        dbase.session.commit()

    def find_all(self, criterion: any, *args, **kwargs):
        # criterion => speciality | location | mode | [speciality, location]
        # args => speciality_name | location | doctor_name
        doctors =  Doctor.query.join(
            Speciality,
            Doctor.id == Speciality.doctor_id, 
        ).join(
            MemberAddress, Doctor.address_id == MemberAddress.id
        ).join(License, License.id == Doctor.id
        ).add_columns(
            Doctor.name, 
            Doctor.nif, 
            Doctor.phone, 
            Doctor.addresses, 
            Speciality.title, 
            Doctor.mode,
            MemberAddress.road,
            MemberAddress.flat,
            MemberAddress.zipcode,
            MemberAddress.city,
            MemberAddress.country            
        )
        if "speciality" in criterion:
            return doctors.filter(Speciality.title == kwargs["name"]).all()
        if criterion == "location": 
            return doctors.filter(MemberAddress.city == kwargs["name"]).all()
        if criterion == "mode":
            return doctors.filter(Doctor.mode == kwargs["mode"]).all()

    @staticmethod  
    def link_speciality(self, session: Session, specialities: any):
        for speciality in specialities:
            check = session.query(Speciality).filter(Speciality.name == speciality.title).first()
            try:
                if check:
                    check.doctors.append(self)
                    return True
                else:
                    new_speciality = Speciality(title=speciality.title, details=speciality.details)
                    self.specialities.append(new_speciality)
                    session.commit()
                    return True
            except:
                session.rollback()
                return None

    @staticmethod
    def link_addresses(self, session: Session, address: any):
        member_address = MemberAddress(address)
        try:
            if member_address.save():
                self.addresses.append(self)
                return True
            else:
               return False
        except:
            session.rollback()
            return None

    @staticmethod
    def link_licenses(self, session: Session, licenses: any):
        for license in licenses:
            new_license = License(license)
            try:
                if new_license.save():
                    self.licenses.append(self)
                    return True
                else:
                    pass
            except:
                session.rollback()
                return None


class Speciality(dbase.Model):
    __tablename__ = "speciality"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String(55), unique=True, nullable=False)
    details = Column(Text(256))
    doctor_id = Column(Integer, ForeignKey("doctor.id", ondelete="CASCADE"))

    def __init__(self, **kwargs):
        self.title = initializer("title", kwargs)
        self.details = initializer("details", kwargs)
        self.doctor_id = initializer("doctor_id", kwargs)

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except:
            return None

    def getby_title(self, title):
        return list([x.name, x.details] for x in Speciality.query.filter(Speciality.title.like(title)))
    
    def getby_id(self, id):
        return list([x.name, x.details] for x in Speciality.query.filter(id == id))

    

class License(dbase.Model):
    __tablename__ = "license"
    __bind_key__ = "profiles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)

    code =  Column(String(128), unique=True) # Encrypted

    issue_date = Column(String(8))

    valid_date = Column(String(8))

    issuer = Column(String(128))

    country = Column(Integer, ForeignKey("country.id"))

    certificate = Column(String(128), default="/media/profiles/licenses/certificate.pdf") # Image path Encrypted
    
    doctor_id = Column(Integer, ForeignKey("doctor.id", ondelete="CASCADE"))

    def __init__(self, **kwargs):
        self.code = initializer("code", kwargs)
        self.issue_date = initializer("issue_date", kwargs)
        self.valid_date = initializer("valid_date", kwargs)
        self.issuer = initializer("issuer", kwargs)
        self.country = initializer("country", kwargs)
        self.certificate = initializer("certificate", kwargs)
        self.doctor_id = initializer("doctor_id", kwargs)

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
    country_code = Column(String(2))
    addresses = relationship("MemberAddress", back_populates="country")


    def __init__(self, **kwargs):
        self.name = initializer("name", kwargs)
        self.country_code = initializer("ccode", kwargs)

    def save(self):
        dbase.session.add(self)
        try:
            dbase.session.commit()
            return self.id
        except RuntimeError as e:
            print("Error Country: ", e.args)
            dbase.session.rollback()
            return None

    def delete(self):
        dbase.session.delete(self)
        try:
            dbase.session.flush(self)
            return 1
        except:
            return 0

    def find_by(self, criterion: any):
        if criterion == "id":
            country = Country.query.filter(Country.id == self.id).first()
        else:
            country = Country.query.filter(Country.name.like(self.name)).first()
        
        if country is None:
            self.save()
            return self

        return country.id

    def bind_address(self, address, session):
        id = self.find_by(criterion="name")
        country = session.query(Country).get(id)

        country.addresses.append(address)
        session.commit()

class MemberAddress(dbase.Model):
    __tablename__ = "address"
    __bind_key__ = "profiles"

    id = Column(Integer, primary_key=True)
    road = Column(String(128))
    flat = Column(String(55))
    zipcode  = Column(String(9))
    city = Column(String(55))
    country_id = Column(Integer, ForeignKey("country.id"))
    country = relationship(Country, foreign_keys=[country_id])

    def __init__(self, **kwargs) -> None:
        self.road = initializer("road", kwargs)
        self.flat = initializer("flat", kwargs)
        self.zipcode = initializer("zipcode", kwargs)
        self.city = initializer("city", kwargs) 
        self.country_ = initializer("country", kwargs)

    def save(self):
        dbase.session.add(self)
        session = dbase.session
        try:
            Country(name=self.country_).bind_address(address=self, session=session)
            return self.id
        except RuntimeError as e:
            print(e)
            dbase.session.rollback()
            return None

    def delete(self):
        dbase.session.delete(self)
        try:
            dbase.session.flush(self)
            return 1
        except:
            return 0