from __future__ import absolute_import
from logging import Logger

from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import or_

from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer
from werkzeug.security import check_password_hash, generate_password_hash


from backend import dbase, initializer


session = dbase.session


class Subscriber(dbase.Model):
    __tablename__ = "subscriber"
    __bind_key__ = "subscribers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_name = Column(String(55), unique=True)
    password = Column(String(128))
    role = Column(String(55))
    public_id = Column(String(128), nullable=False, unique=True)
    phone = Column(String(16))
    country = Column(String(55))
    full_name = Column(String(128))
    birth_date = Column(String(12))
    gender = Column(String(6))
    status = Column(String(55))

    access_keys = relationship("AuthenticationKey", backref="subscriber", lazy="select")

    def __init__(self, **kwargs):
        # super().__init__(**kwargs["data"])
        self.user_name = initializer("username", kwargs["data"])
        self.password = initializer("password", kwargs["data"])
        self.role = initializer("role", kwargs["data"])
        self.public_id = initializer("publicid", kwargs["data"])
        self.phone = initializer("phone", kwargs["data"])
        self.country = initializer("country", kwargs["data"])
        self.full_name = initializer("fullname", kwargs["data"])
        self.birth_date = initializer("birthdate", kwargs["data"])
        self.gender = initializer("gender", kwargs["data"])

    def save(self):

        try:
            self.status = "Pending"
            session.add(self)
            session.commit()
            return self
        except RuntimeError as error:
            print(error)
            return None

    def validate(self):
        try:
            subscriber = self.query.filter(
                and_(
                    Subscriber.role.in_(["doctor", "beneficiary", "caregiver"]),
                    Subscriber.user_name.like(self.user_name),
                    Subscriber.public_id.like(self.public_id),
                )
            ).one_or_none()
            if subscriber:
                return True, subscriber
            return False, None
        except RuntimeError as error:
            print(error)
            return False, None

    def get_one(self, userid: str, role: str):
        # print(userid)
        return (
            session.query(Subscriber)
            .filter(Subscriber.role.like(role), Subscriber.user_name.like(userid))
            .first()
        )

    def getby_publicid(self):
        return self.query.filter(
            Subscriber.public_id.like(self.public_id)
        ).one_or_none()

class AuthenticationKey(dbase.Model):

    """Store registered users hashed nif as private_key
    and public_id as public_key.
    """

    __tablename__ = "authentication_keys"
    __bind_key__ = "subscribers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    private_key = Column(String(256), nullable=False)
    subscriber_id = Column("subscriber_id", ForeignKey(Subscriber.id))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    
    def save(self, subscriber=None):  
        try:
            check = self.query.filter(
                AuthenticationKey.private_key.ilike(self.private_key)
            ).first()

            if check:
                
                return True, check
            
            session.add(self)
            subscriber.access_keys.append(self)
            session.commit()
            return True, self

        except RuntimeError as error:
            print(error)
            return False, None

    
    def link_keys_to_subscriber(self, current_user: Subscriber):
        try:
            status, keys = self.save(current_user)
            if status:
                
                return True, keys
            return False, keys
        except RuntimeError as error:
            print(error) 
            return False, None


    def check_keys_link_to_subscriber(self, public_key):
        return Subscriber(public_id=public_key).getby_publicid()
        

    def update(self, private_key, public_key):
        session.query(AuthenticationKey).update(private_key=private_key, public_key=public_key)