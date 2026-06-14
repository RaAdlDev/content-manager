from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.security import hash_password, verify_password, create_token
from schemas.user import UserLogin
from schemas.token import TokenResponse


def register_user(db: Session, user: UserCreate):
    role = "READER"
    first_user = db.execute(select(User)).scalars().all()
    if not first_user:
        role = "ADMIN"
    user_unique = db.execute(select(User).where((User.email == user.email))).scalar_one_or_none()
    if not user_unique:
        db.add(User(email = user.email, hashed_password = hash_password(user.password), role = role))
        db.commit()
        return True
    return None


def login_user(db: Session, form: UserLogin):
    user_data = db.execute(select(User).where(User.email == form.email)).scalar_one_or_none()
    if user_data:
        if verify_password(form.password, user_data.hashed_password):
            return TokenResponse(token= create_token({"sub": user_data.user_id, "role": user_data.role}), token_type= "bearer")
        return None
    return None

def inactive_user(db: Session, user_id: str):
    user = db.get(User, user_id)
    if not user:
        return "NOT_FOUND"
    if user.is_active == False:
        return "INVALID_STATUS"
    user.is_active = False
    db.commit()
    return True

def to_writer(db: Session, user_id: str):
    user = db.get(User, user_id)
    if not user:
        return "NOT_FOUND"
    if user.role == "READER":
        user.role == "WRITER"
        db.commit()
        return True
    return "INVALID_STATUS"


def to_admin(db: Session, user_id: str):
    user = db.get(User, user_id)
    if not user:
        return "NOT_FOUND"
    if user.role == "ADMIN":
        return "INVALID_STATUS"
    user.role == "ADMIN"
    db.commit()
    return True