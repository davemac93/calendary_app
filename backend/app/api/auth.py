from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List


from ..schemas import RegisterUser
from ..models import User
from ..core import create_access_token, verify_token, authenticate_user, get_password_hash, validate_username_unique, validate_user_exists
from ..db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def create_user(user_data: RegisterUser, db: Session = Depends(get_db)):
    validate_username_unique(db, user_data.username)
    user = User(
        username=user_data.username,
        password=get_password_hash(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
def get_profile(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    user_id = verify_token(token, credentials_exception)
    return {"user_id": user_id}