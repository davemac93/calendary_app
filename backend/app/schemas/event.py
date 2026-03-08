from pydantic import BaseModel

class CreateEvent(BaseModel):
    title: str
    start_date: str
    end_date: str
    description: str