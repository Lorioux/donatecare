from sqlalchemy import Column, Integer, String

import sys

sys.path.append("..")

from backend.databases import dbase


class Appointment(dbase.Model):
    __tablename__ = "appointments"
    __table_args__ = {"extend_existing": True}
    __bind_key__ = "booking"

    id = Column(dbase.Integer, primary_key=True)
    date = Column(dbase.String(8))
    time = Column(dbase.String(5))
    doctName = Column(dbase.String(55))
    doctSpeciality = Column(dbase.String(55))
    doctIdentity = Column(dbase.String(128))
    doctAddress = Column(dbase.String(128))
    beneficiaryName = Column(dbase.String(55))
    beneficiaryPhone = Column(dbase.String(12))
    beneficiaryNif = Column(dbase.String(128))

    def __init__(
        self,
        date,
        time,
        doctName,
        doctSpeciality,
        doctIdentity,
        beneficiaryName,
        beneficiaryPhone,
        beneficiaryNif,
    ):
        self.date = date
        self.time = time
        self.doctName = doctName
        self.doctSpeciality = doctSpeciality
        self.doctIdentity = doctIdentity
        self.beneficiaryName = beneficiaryName
        self.beneficiaryPhone = beneficiaryPhone
        self.beneficiaryNif = beneficiaryNif

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()
