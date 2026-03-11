from datetime import datetime, timedelta
from jose import JWTError, jwt
from pwdlib.exceptions import UnknownHashError

from sqlalchemy.orm import Session

from .config import settings
from .security import verify_password


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


def authenticate_user(db: Session, username: str, password: str):
    from ..models import User
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    try:
        # If verify_password fails due to a bad hash format, it triggers the except block
        if not verify_password(password, user.password):
            return None
    except (UnknownHashError, ValueError, TypeError):
        # We catch the traceback here and return None to signal 'auth failed'
        return None

    return user

def check_user_exists(db: Session, username: str) -> bool:
    from ..models import User
    return db.query(User).filter(User.username == username).first() is not None