from sqlalchemy.orm import Session
from schemas.category import CategoryInput
from models.category import Category
from sqlalchemy import select
from slugify import slugify

def create_category(db: Session, category_data: CategoryInput):
    exists = db.execute(select(Category).where(Category.name == category_data.name)).scalar_one_or_none()
    if exists:
        return None
    slug = slugify(category_data.name)
    new_category = Category(
        name = category_data.name,
        slug = slug
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def view_categories(db: Session):
    categories = db.execute(select(Category)).scalars().all()
    return categories