from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import CreateEvent, UpdateEvent, ResponseEvent
from ..models import Event
from ..core import get_db

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("/", response_model=List[ResponseEvent])
async def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events


@router.post("/add", response_model=ResponseEvent)
async def create_event(event_data: CreateEvent, db: Session = Depends(get_db)):
    event = Event(
        title=event_data.title,
        start_date=event_data.start_date,
        end_date=event_data.end_date,
        description=event_data.description,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/{id}", response_model=ResponseEvent)
async def get_event(id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.put("/{id}", response_model=ResponseEvent)
async def update_event(id: int, event_data = UpdateEvent, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.title is not None:
        event.title = event_data.title
    if event.start_date is not None:
        event.start_date = event_data.start_date
    if event.end_date is not None:
        event.end_date = event_data.end_date
    if event.description is not None:
        event.description = event_data.description

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()

    return None
