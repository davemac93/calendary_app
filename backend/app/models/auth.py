from sqlalchemy import Column, Integer, String
from uuid import uuid4

from ..core import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


