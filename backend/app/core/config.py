import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "")
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "")


settings = Config()