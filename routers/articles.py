from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from models.user import User
from dependencies.roles import get_writer, get_admin
from dependencies.auth import get_current_user
from database.connection import get_db
from schemas.article import CreateArticle, ArticleResponse, ArticleUpdate, PaginationResponse
from services.articles_services import new_article, pages_search, my_articles, update_article, submit_draft_rejected, publish_article, article_to_reject, soft_delete, view_one
from typing import Optional
from schemas.rejection import RejectionInput
from services.notifications_services import new_notification

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/", response_model=ArticleResponse)
async def post_article(article_data: CreateArticle, current_user: User = Depends(get_writer), db: Session = Depends(get_db)):
    return new_article(db, article_data, current_user)

@router.get("/", response_model=PaginationResponse[ArticleResponse])
async def get_articles(search: Optional[str] = None, category: Optional[str] = None, tags: Optional[list[str]] = None, page:int = Query(1, ge=1, description="page"), size: int = Query(10, ge=1, le=100, description="size_page"), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    status = pages_search(db, current_user, page, size, category, tags, search)
    if status is None:
            raise HTTPException(status_code=404, detail="The Page Doesn't Exist")
    return status

@router.get("/my-articles", response_model=list[ArticleResponse])
async def get_my_articles(current_user: User = Depends(get_writer), db: Session = Depends(get_db)):
    return my_articles(db, current_user)

@router.get("/{article_id}", response_model=ArticleResponse)
async def get_articles(article_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    status =  view_one(db, current_user, article_id)
    if status is None:
         raise HTTPException(status_code=409, detail="Article Isn't Aviable")
    return status

@router.patch("/{article_id}", response_model=ArticleResponse)
async def patch_article(article_id: str, update_data: ArticleUpdate , current_user: User = Depends(get_writer), db: Session = Depends(get_db)):
    status = update_article(db, update_data, article_id, current_user)
    if status == "FORBIDDEN":
         raise HTTPException(status_code=403, detail="Not Allowed")
    if status == "NOT_FOUND":
         raise HTTPException(status_code=404, detail="Article Not Found")
    if status == "INVALID_STATUS":
         raise HTTPException(status_code=409, detail="Invalid Article Status")
    return status

@router.post("/{article_id}/submit", response_model=ArticleResponse)
async def submit_article(article_id: str, current_user: User = Depends(get_writer), db: Session = Depends(get_db)):
    status = submit_draft_rejected(db, article_id, current_user)
    if status == "FORBIDDEN":
         raise HTTPException(status_code=403, detail="Not Allowed")
    if status == "NOT_FOUND":
         raise HTTPException(status_code=404, detail="Article Not Found")
    if status == "INVALID_STATUS":
         raise HTTPException(status_code=409, detail="Invalid Article Status")
    return status

@router.post("/{article_id}/approve", response_model=ArticleResponse)
async def approve_article(background: BackgroundTasks, article_id: str, current_user: User = Depends(get_admin), db: Session = Depends(get_db)):
    results, notification = publish_article(db, article_id)
    if results == "NOT_FOUND":
         raise HTTPException(status_code=404, detail="Article Not Found")
    if results == "INVALID_STATUS":
         raise HTTPException(status_code=409, detail="Invalid Article Status")
    background.add_task(new_notification, notification)
    return results

@router.post("/{article_id}/reject")
async def reject_article(background: BackgroundTasks, rejection_reason: RejectionInput, article_id: str, current_user: User = Depends(get_admin), db: Session = Depends(get_db)):
    results, notification = article_to_reject(db, article_id, rejection_reason)
    if results == "NOT_FOUND":
         raise HTTPException(status_code=404, detail="Article Not Found")
    if results == "INVALID_STATUS":
         raise HTTPException(status_code=409, detail="Invalid Article Status")
    background.add_task(new_notification, notification)
    return results
@router.delete("/{article_id}")
async def delete_article(article_id: str, current_user: User = Depends(get_admin), db: Session = Depends(get_db)):
    status = soft_delete(db, article_id)
    if status is None:
                raise HTTPException(status_code=404, detail="Article Not Found")
    return status




