from pydantic import BaseModel
from typing import Optional

class CreateEvent(BaseModel):
    title: str
    start_date: str
    end_date: str
    description: str

class UpdateEvent(BaseModel):
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ResponseEvent(BaseModel):
    id: int
    title: str
    start_date: str
    end_date: str
    description: Optional[str] = None

    class Config:
        from_attributes = True







