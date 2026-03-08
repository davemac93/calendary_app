from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..schemas import CreateEvent
from ..models import Event
from ..core import get_db

router = APIRouter(prefix="/event", tags=["Event"])

@router.post("")
async def create_event(event_data: CreateEvent, db: Session = Depends(get_db)):
    event = Event(
        title=event_data.title,
        start_date=event_data.start_date,
        end_date=event_data.end_date,
        description=event_data.description
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"message": "Event created"}