from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app import models
from .config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + (settings.JWT_ACCESS_TOKEN_EXPIRES or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user