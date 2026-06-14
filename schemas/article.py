from pydantic import BaseModel, ConfigDict
from typing import Optional, TypeVar, Generic, List, Literal
from datetime import datetime

T = TypeVar('T')
class CreateArticle(BaseModel):
    title: str
    content: str
    tags: Optional[list[str]] = None
    category_id: Optional[str] = None


class ArticleResponse(BaseModel):
    title: str
    content: str
    tags: Optional[list[str]] = None
    category_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    article_id: str
    author_id: str
    status: Literal["DRAFT", "PENDING_REVIEW", "PUBLISHED", "REJECTED"]

    model_config = ConfigDict(from_attributes=True)


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[str] =None
    tags: Optional[list[str]] = None

class PaginationMeta(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_previous: bool

class PaginationResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta