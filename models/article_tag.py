from models.base import Base
from sqlalchemy import ForeignKey, Table, Column, String



article_tag = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", String, ForeignKey("article.article_id"), primary_key = True),
    Column("tag_id", String,  ForeignKey("tag.tag_id"), primary_key = True)

    )