from fastapi import APIRouter, Depends, HTTPException
from dependencies.roles import get_admin
from database.connection import get_db
from sqlalchemy.orm import Session
from schemas.category import CategoryInput, CategoryOutput
from models.user import User
from services.category_services import create_category, view_categories

router = APIRouter(prefix="/category", tags=["Category"])

@router.post("/", response_model= CategoryOutput)
async def new_category(data: CategoryInput, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    status = create_category(db, data)
    if status is None:
        raise HTTPException(status_code=404, detail="Category Already Exists")
    return status

@router.get("/", response_model= list[CategoryOutput])
async def get_category(db: Session = Depends(get_db)):
    return view_categories(db)
    