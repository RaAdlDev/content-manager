from fastapi import APIRouter, Depends, HTTPException
from dependencies.roles import get_admin
from database.connection import get_db
from sqlalchemy.orm import Session
from schemas.tag import TagInput, TagOutput
from models.user import User
from services.tags_services import view_tags, create_tag


router = APIRouter(prefix="/tag", tags=["Tag"])

@router.post("/", response_model=TagOutput)
async def new_tag(data: TagInput, db: Session = Depends(get_db), current_user: User = Depends(get_admin)):
    status = create_tag(db, data)
    if status is None:
        raise HTTPException(status_code=404, detail="Tag Already Exists")
    return status

@router.get("/", response_model=list[TagOutput])
async def new_tag(db: Session = Depends(get_db)):
    return view_tags(db)

