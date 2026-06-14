from dependencies.auth import get_current_user
from models.user import User
from fastapi import Depends, HTTPException

def get_writer(user: User = Depends(get_current_user)):
    if user.role not in ["WRITER", "ADMIN"]:
        raise HTTPException(status_code=403, detail="You Are Not Allowed")       
    return user

def get_admin(user: User = Depends(get_current_user)):
    if user.role == "ADMIN":
        return user
    raise HTTPException(status_code=403, detail="You Are Not Allowed")

