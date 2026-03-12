import uuid
from typing import List

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class User(Base):

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String)

    events: Mapped[List["Event"]] = relationship(back_populates="user")


