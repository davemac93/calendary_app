from datetime import datetime, timedelta
from jose import JWTError, jwt
from backend.app.core.security import verify_password
from sqlalchemy.orm import Session

from backend.app import models
from .config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (settings.JWT_ACCESS_TOKEN_EXPIRES or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str, credentials_exception) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

def authenticate_user(db: Session, username: str, password: str) -> models.User | bool:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    
    return user

def check_user_exists(db: Session, username: str) -> bool:
    return db.query(models.User).filter(models.User.username == username).first() is not None