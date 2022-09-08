from common.db import Base
from common.db.mixins import TimestampMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


# sqlalchemy class User, table in db users
class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "email": self.email
        }