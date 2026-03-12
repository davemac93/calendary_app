from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .auth import oauth2_scheme
from ..core import verify_token
from ..schemas import ResponseEvent
from ..db import get_db
from ..core.crud import update_event_status, get_events_by_userid

router = APIRouter(prefix="/api/public", tags=["owner_events"])



@router.get("/{username}/all_events", response_model=List[ResponseEvent])
async def update_event(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    user_id = verify_token(token, credentials_exception)
    event = get_events_by_userid(db, user_id)

    return event

@router.put("/{username}/{event_id}/accept", response_model=ResponseEvent)
def accept_event(event_id: UUID, db: Session = Depends(get_db)):
    db_event = update_event_status(db, event_id, True)

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    return db_event

@router.delete("/{username}/{event_id}/cancel", response_model=ResponseEvent)
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    db_event = delete_event(db, event_id)

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    return db_event