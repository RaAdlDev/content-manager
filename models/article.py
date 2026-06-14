from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum
from typing import Literal, List, Optional
from datetime import datetime
from sqlalchemy import func, ForeignKey, String
import uuid

class Article(Base):
    __tablename__="article"
    article_id: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid.uuid4()))
    author_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    category_id: Mapped[Optional[str]] = mapped_column(ForeignKey("category.category_id"), nullable=True)
    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
    status: Mapped[Literal["DRAFT", "PENDING_REVIEW", "PUBLISHED", "REJECTED"]] = mapped_column(
        Enum("DRAFT", "PENDING_REVIEW", "PUBLISHED", "REJECTED", name="article_status_types")
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    tags: Mapped[List["Tag"]] = relationship(secondary="article_tag", back_populates="articles")
    user: Mapped["User"] = relationship(back_populates="user_articles")







