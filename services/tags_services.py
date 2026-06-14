from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.tag import TagInput
from models.tag import Tag
from slugify import slugify


def create_tag(db:Session, tag_data: TagInput):
    exists = db.execute(select(Tag).where(Tag.name == tag_data.name)).scalar_one_or_none()
    if exists:
        return None
    slug = slugify(tag_data.name)
    new_tag = Tag(
        name = tag_data.name,
        slug = slug
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


def view_tags(db: Session):
    tags = db.execute(select(Tag)).scalars().all()
    return tags