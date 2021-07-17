from operator import and_
import sys

sys.path.append("..")

from sqlalchemy import Column, String, Integer

from backend import dbase, initializer


class Schedule(dbase.Model):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "schedule"
    __bind_key__ = "schedules"

    id = Column(Integer, primary_key=True)
    date = Column(String(11))
    time = Column(String(11))
    week = Column(Integer)
    year = Column(Integer)
    doctor_id = Column(Integer)

    def __init__(self, **kwargs):
        self.date = initializer("date", kwargs)
        self.time = initializer("time", kwargs)
        self.year = initializer("year", kwargs)
        self.week = initializer("week", kwargs)
        self.doctor_id = initializer("doctor_id", kwargs)

    def save(self):
        dbase.session.add(self)
        dbase.session.commit()

    def getby_date(self, date):
        return Schedule.query.filter(date == date)

    def getby_date_time(self, date, time):
        return Schedule.query.filter(
            and_(Schedule.date.like(date), Schedule.time.like(time))
        )

    def getby_week(self, week, year, id=None):
        if id:
            return Schedule.query.filter(
                and_(
                    Schedule.week >= week,
                    Schedule.year <= year,
                    Schedule.doctor_id == id,
                )
            )
        return Schedule.query.filter(and_(Schedule.week >= week, Schedule.year <= year))
