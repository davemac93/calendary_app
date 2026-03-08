from sqlalchemy import Column, Integer, String

from ..core import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)

