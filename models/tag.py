from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import List

class Tag(Base):
    __tablename__="tag"
    tag_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)

    articles: Mapped[List["Article"]] = relationship(secondary="article_tag", back_populates="tags")


 