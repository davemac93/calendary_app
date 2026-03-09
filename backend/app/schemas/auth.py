from pydantic import BaseModel

class RegisterUser(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class RespondUser(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        from_attributes = True