from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List


from sqlalchemy.testing.pickleable import User

from ..schemas import RegisterUser, LoginUser
from ..models import User
from ..core import get_db, create_access_token, verify_token, authenticate_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def create_user(user_data: RegisterUser, db: Session = Depends(get_db)):
    user = User(
        username=user_data.username,
        password=user_data.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[RegisterUser])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    user_id = verify_token(token, credentials_exception)
    return {"user_id": user_id}