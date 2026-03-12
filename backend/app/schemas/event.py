from uuid import UUID

from pydantic import BaseModel
from typing import Optional

class CreateEvent(BaseModel):
    title: str
    start_date: str
    end_date: str
    description: str
    email: str

class UpdateEvent(BaseModel):
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ResponseEvent(BaseModel):
    id: UUID
    title: str
    start_date: str
    end_date: str
    user_id: UUID
    email: str
    description: Optional[str] = None
    accepted: Optional[bool] = False

    class Config:
        from_attributes = True







