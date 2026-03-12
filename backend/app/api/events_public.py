from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import CreateEvent, ResponseEvent
from ..db import get_db
from ..core.auth import validate_user_exists
from ..core.crud import create_event, get_events_by_email

router = APIRouter(prefix="/api/public/events", tags=["public-events"])


@router.post("/{username}/book", response_model=ResponseEvent)
def book_event_route(username: str, event: CreateEvent,  db: Session = Depends(get_db)):
    user = validate_user_exists(db, username)
    event = create_event(db, event, user.id)
    return event

@router.get("/search/{email}", response_model=list[ResponseEvent])
def find_my_bookings(email: str, session: Session = Depends(get_db)):
    return get_events_by_email(session, email)