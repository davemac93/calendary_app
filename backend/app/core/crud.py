from sqlalchemy.orm import Session
from uuid import UUID

from ..models.user import User
from ..schemas import CreateEvent
from ..models.event import Event

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_event(db: Session, event: CreateEvent, user_id: UUID):

    db_event = Event(
        **event.model_dump(),
        user_id=user_id,
        accepted=False
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events_by_email(db: Session, email: str):
    return db.query(Event).filter(Event.email == email).all()

def get_events_by_userid(db: Session, user_id: UUID):
    return db.query(Event).filter(Event.user_id == user_id).all()

def delete_event(db: Session, event_id: UUID) -> bool:
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        db.refresh(db_event)
        return True
    return False

def update_event_status(db: Session, event_id: UUID, accepted: bool):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event:
        db_event.accepted = accepted
        db.commit()
        db.refresh(db_event)
    return db_event