from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.settings import settings
from jose import jwt
from datetime import datetime, timedelta, timezone


oauth = OAuth2PasswordBearer(tokenUrl="auth/login")


password_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain):
    return password_context.hash(plain)

def verify_password(plain_password, data_password):
    return password_context.verify(plain_password, data_password)

def create_token(data: dict):
    to_encode = data.copy()
    time = datetime.now(timezone.utc) + timedelta(minutes= settings.token_duration)
    to_encode.update({"exp": time})
    return jwt.encode(to_encode, settings.secret_key, settings.algorithm)





