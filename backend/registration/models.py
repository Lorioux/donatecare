from sqlalchemy import Column, String, Integer
from enum import unique

import sys
sys.path.append("..")

from backend.databases import dbase

class Beneficiaries(dbase.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "beneficiaries"
    __bind_key__ = "registration"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(55))
    age = Column(Integer)
    phone = Column(String(55))
    nif = Column(String(55), unique=True)

    def __init__(self, fullname, age, phone, nif):
        self.fullname = fullname
        self.age = age
        self.phone = phone
        self.nif = nif

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()