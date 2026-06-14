from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.settings import settings

engine = create_engine(settings.database_url)

LocalSesion = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = LocalSesion()
    try:
        yield db
    except Exception:
        db.rollback()
        raise 
    finally: 
        db.close()
    