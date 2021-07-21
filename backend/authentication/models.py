from __future__ import absolute_import
from logging import Logger

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.sql.elements import and_

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Integer
from werkzeug.security import generate_password_hash


from backend import dbase, initializer


session = dbase.session


class Subscriber(dbase.Model):
    __tablename__ = "subscriber"
    __bind_key__ = "subscribers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    user_name = Column(String(55))
    password = Column(String(128))
    role = Column(String(55))
    public_id = Column(String(128), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_name = initializer("user_name", kwargs)
        self.password = initializer("password", kwargs)
        self.role = initializer("role", kwargs)
        self.public_id = initializer("public_id", kwargs)

    def save(self):
        valid, subscriber = self.validate()
        if not valid:
            session.add(self)
            session.commit()
            return self
        return subscriber

    def validate(self):
        subscriber = self.query.filter(
            and_(
                Subscriber.password.like(generate_password_hash(self.password)),
                Subscriber.role.in_(["doctor", "beneficiary"]),
            ),
            and_(
                Subscriber.user_name.like(self.user_name),
                Subscriber.public_id.like(self.public_id),
            ),
        ).first()
        if subscriber is not None:
            return True, subscriber
        return False, None


class AuthenticationKey (dbase.Model):

    """Store registered users hashed nif as private_key
    and public_id as public_key.
    """

    __tablename__ = "authentication_keys"
    __bind_key__ = "subscribers"
    __table_args__ = {"extend_existing":True}

    id = Column(Integer, primary_key=True)
    private_key = Column(String(256), nullable=False)
    public_key = Column(String(128), nullable=False)
    # subscribe = relationship("Subscriber", back_populates="authentication_keys")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def save(self):
        check = self.query.filter(
            and_(
                AuthenticationKey.private_key.like(self.private_key),
                AuthenticationKey.public_key.like(self.public_key)
            )
        ).one_or_none()

        if check:
            return True, check
        session.add(self)
        try:
            session.commit()
            return True, self
        except RuntimeError as error:
            Logger("AUTH_KEYS").error(error)
            return False, None