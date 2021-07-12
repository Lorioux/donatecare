from sqlalchemy import Column, Integer, String

import sys

sys.path.append("..")

from backend.databases import dbase, initializer


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

    def __init__(self, **kwargs    ):
        self.date = initializer("date", kwargs)
        self.time = initializer("time", kwargs)
        self.doctName = initializer("doctName", kwargs)
        self.doctSpeciality = initializer("doctSpeciality", kwargs)
        self.doctIdentity = initializer("doctIdentity", kwargs)
        self.beneficiaryName = initializer("beneficiaryName", kwargs)
        self.beneficiaryPhone = initializer("beneficiaryPhone", kwargs)
        self.beneficiaryNif = initializer("beneficiaryNif", kwargs)

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()
