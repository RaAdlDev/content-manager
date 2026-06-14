from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import Literal, List
from datetime import datetime
from sqlalchemy import func, Enum

class User(Base):
    __tablename__="users"
    user_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Literal["READER", "WRITER", "ADMIN"]] = mapped_column(
        Enum("READER", "WRITER", "ADMIN", name="role_types")
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_articles: Mapped[List["Article"]] = relationship(back_populates="user")






