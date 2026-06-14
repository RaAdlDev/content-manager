from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import String


class Category(Base):
    __tablename__="category"
    category_id:  Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(30), unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    