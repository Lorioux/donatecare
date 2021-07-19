from __future__ import absolute_import
from flask.globals import session
from flask_sqlalchemy import BaseQuery

from sqlalchemy import Column, Integer, String

# import sys
# sys.path.append("..")

from backend import dbase, initializer

session = dbase.session


class Appointment(dbase.Model):
    __tablename__ = "appointments"
    __table_args__ = {"extend_existing": True}
    __bind_key__ = "booking"

    id = Column(Integer, primary_key=True)
    date = Column(String(8))
    time = Column(String(5))
    doct_name = Column(String(55))
    doct_speciality = Column(String(55))
    doct_identity = Column(String(128))
    doct_address = Column(String(128))
    beneficiary_name = Column(String(55))
    beneficiary_phone = Column(String(12))
    beneficiary_nif = Column(String(128))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = initializer("date", kwargs)
        self.time = initializer("time", kwargs)
        self.doct_name = initializer("doctName", kwargs)
        self.doct_speciality = initializer("doctSpeciality", kwargs)
        self.doct_identity = initializer("doctIdentity", kwargs)
        self.beneficiary_name = initializer("beneficiaryName", kwargs)
        self.beneficiary_phone = initializer("beneficiaryPhone", kwargs)
        self.beneficiary_nif = initializer("beneficiaryNif", kwargs)

    def save(self):
        session.add(self)
        session.commit()
