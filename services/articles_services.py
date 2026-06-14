from sqlalchemy.orm import Session
from schemas.article import CreateArticle, ArticleUpdate, PaginationMeta, PaginationResponse
from models.article import Article
from models.user import User
from sqlalchemy import select, func
from datetime import datetime, timezone
from math import ceil
from typing import Optional
from models.tag import Tag
from schemas.rejection import RejectionInput
from services.notifications_services import new_notification
from schemas.notification import NotificationInput
import asyncio
from fastapi import BackgroundTasks

def new_article(db: Session, article_data: CreateArticle, current_user: User): 
    tags = [] 
    if article_data.tags:
        tags = db.execute(select(Tag).where(Tag.tag_id.in_(article_data.tags))).scalars().all()
    article_info = Article(
        author_id = current_user.user_id, 
        title = article_data.title, 
        content = article_data.content,
        status = "DRAFT",
        category_id = article_data.category_id,
        tags = tags)
    
    db.add(article_info)
    db.commit()
    db.refresh(article_info)
    return article_info


def pages_search(db: Session, current_user:User, page: int, size: int, category_id: Optional[str], tags: Optional[list[str]], search: Optional[str]):

    offset = (page - 1) *size
    query = select(Article).where(Article.deleted_at.is_(None))
    if search:
        query = query.where(Article.title.ilike(f"%{search}%"))
    if category_id:
        query = query.where(Article.category_id == category_id)
    if tags:
        query = query.where(Article.tags.any(Tag.tag_id.in_(tags)))
    if current_user.role != "ADMIN":
        query = query.where(Article.status == "PUBLISHED")
    
    len_items = db.execute(select(func.count()).select_from(query.subquery())).scalar_one()
    if len_items <= offset:
        return None
    items = db.execute(query.offset(offset).limit(size)).scalars().all()
    total_pages = ceil(len_items/size) if len_items > 0 else 1
    meta = PaginationMeta(
        total_items=len_items,
        total_pages=total_pages,
        current_page= page,
        page_size=size,
        has_next= total_pages > page ,
        has_previous= page > 1
    )
    return PaginationResponse(
        data = items,
        meta= meta
    )


def my_articles(db: Session, current_user: User):
    user_articles = db.execute(select(Article).where(Article.author_id == current_user.user_id)).scalars().all()
    return user_articles


def update_article(db: Session, update_data: ArticleUpdate, article_id: str, current_user: User):
    article_update = db.get(Article, article_id)
    if not article_update:
        return "NOT_FOUND"
    if article_update.author_id != current_user.user_id:
        return "FORBIDDEN"
    if article_update.status not in ["REJECTED", "DRAFT"]:
        return "INVALID_STATUS"
    if update_data.title:
        article_update.title = update_data.title
    if update_data.content:
        article_update.content = update_data.content
    if update_data.category_id:
        article_update.category_id = update_data.category_id
    if update_data.tags:
        tags = db.execute(select(Tag).where(Tag.tag_id.in_(update_data.tags))).scalars().all()
        article_update.tags = tags
    db.commit()
    db.refresh(article_update)
    return article_update

def submit_draft_rejected(db: Session, article_id: str, current_user: User):
    submit_article = db.get(Article, article_id)
    if not submit_article:
        return "NOT_FOUND"
    if submit_article.author_id != current_user.user_id:
        return "FORBIDDEN"
    if not submit_article.status in ["DRAFT", "REJECTED"]:
        return "INVALID_STATUS"
    submit_article.status = "PENDING_REVIEW"
    db.commit()
    return submit_article
    
def publish_article(db: Session, article_id: str):
    notification = None
    article_to_publish = db.get(Article, article_id)
    if not article_to_publish:
        status = "NOT_FOUND"
        return status, notification
    if article_to_publish.status != "PENDING_REVIEW":
        status = "INVALID_STATUS"
        return status, notification
    article_to_publish.status = "PUBLISHED"
    article_to_publish.published_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(article_to_publish)
    notification = NotificationInput(writer_user_id= article_to_publish.author_id,
        article_id= article_to_publish.article_id,
        message= f"your article {article_to_publish.title} has been published")
    return article_to_publish, notification

def article_to_reject(db: Session,  article_id: str, rejection: RejectionInput):
    notification = None
    article_to_reject= db.get(Article, article_id)
    if not article_to_reject:
        status =  "NOT_FOUND"
        return status, notification
    if article_to_reject.status != "PENDING_REVIEW":
        status = "INVALID_STATUS"
        return status, notification
    article_to_reject.status ="REJECTED"
    article_to_reject.rejection_reason = rejection.rejection_reason
    db.commit()
    db.refresh(article_to_reject)
    notification = NotificationInput(writer_user_id= article_to_reject.author_id,
        article_id= article_to_reject.article_id,
        message= f"{article_to_reject.status}, reason: {article_to_reject.rejection_reason}")
    return article_to_reject, notification


def soft_delete(db: Session, article_id: str):
    article_to_reject= db.get(Article, article_id)
    if not article_to_reject:
        return None
    article_to_reject.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return article_to_reject

def view_one(db: Session, current_user: User, article_id: str):
    article = db.get(Article, article_id)
    if not article:
        return None
    if article.status == "PUBLISHED":
        return article
    if current_user.role == "ADMIN":
        return article
    if current_user.role == "WRITER":
        if article.author_id == current_user.user_id:
            return article
    return None


