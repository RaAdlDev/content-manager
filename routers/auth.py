from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from database.connection import get_db
from services.auth_services import register_user, login_user, inactive_user, to_admin, to_writer
from models.user import User
from dependencies.roles import get_admin
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(data: UserCreate, db: Session = Depends(get_db)):
    status = register_user(db, data)
    if status is None:
        raise HTTPException(status_code=409, detail="Try Another Data")
    return {"status": "Successful Request"}


@router.post("/login")
async def login(form: UserLogin, db: Session = Depends(get_db)):
    status = login_user(db, form)
    if status is None:
        raise HTTPException(status_code=401, detail="The Data is Incorrect")
    return status

@router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    status = inactive_user(db, user_id)
    if status == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="User Not Found")
    if status == "INVALID_STATUS":
        raise HTTPException(status_code=409, detail="User Already Inactive")
    return {"status": "Successful Request"}

@router.patch("/{user_id}/writer")
async def new_writer(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    status = to_writer(db, user_id)
    if status == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="User Not Found")
    if status == "INVALID_STATUS":
        raise HTTPException(status_code=409, detail="Invalid User Role")
    return {"status": "Successful Request"}
@router.patch("/{user_id}/admin")
async def new_admin(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    status = to_admin(db, user_id)
    if status == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="User Not Found")
    if status == "INVALID_STATUS":
        raise HTTPException(status_code=409, detail="Invalid User Role")
    return {"status": "Successful Request"}