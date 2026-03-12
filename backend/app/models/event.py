import uuid

from sqlalchemy import ForeignKey, UUID, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base



class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="events")

