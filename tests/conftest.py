import pytest 
from core.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.connection import get_db
from main import app
from models.base import Base
from fastapi.testclient import TestClient
from models.user import User
from core.security import hash_password, create_token
from sqlalchemy.orm import Session
from unittest.mock import patch, AsyncMock

engine = create_engine(settings.testing_database_url)

LocalSessionTest = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = LocalSessionTest(bind=connection)

    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    def get_override():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = get_override

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def create_writer_admin_reader(db_session: Session):
    hashed_password = hash_password("Test123*")
    new_writter = User(
        role= "WRITER",
        email= "example@example.com",
        hashed_password = hashed_password
    )
    new_admin = User(
        role= "ADMIN",
        email= "example@example2.com",
        hashed_password = hashed_password
    )
    new_reader= User(
        role= "READER",
        email= "example@example3.com",
        hashed_password = hashed_password
    )

    db_session.add_all([new_admin, new_writter, new_reader])
    db_session.commit()
    return {
        "admin": new_admin,
        "writer": new_writter,
        "reader": new_reader
    }

@pytest.fixture()
def reader_token(create_writer_admin_reader):
    user = create_writer_admin_reader["reader"]

    token = create_token({"sub": user.user_id})

    return token

@pytest.fixture()
def writer_token(create_writer_admin_reader):
    user = create_writer_admin_reader["writer"]

    token = create_token({"sub": user.user_id})

    return token

@pytest.fixture()
def admin_token(create_writer_admin_reader):
    user = create_writer_admin_reader["admin"]

    token = create_token({"sub": user.user_id})

    return token

@pytest.fixture()
def client_admin(client, admin_token):
    client.headers.update({"Authorization": f"Bearer {admin_token}"})

    yield client

    client.headers.pop("Authorization", None)

@pytest.fixture()
def client_writer(client, writer_token):
    client.headers.update({"Authorization": f"Bearer {writer_token}"})

    yield client

    client.headers.pop("Authorization", None)

@pytest.fixture()
def reader_client(client, reader_token):
    client.headers.update({"Authorization": f"Bearer {reader_token}"})

    yield client

    client.headers.pop("Authorization", None)

@pytest.fixture()
def article_submit(admin_token):
    admin_client = TestClient(app)
    admin_client.headers.update({"Authorization": f"Bearer {admin_token}"})
  
    article = admin_client.post("/articles", json={"title": "yes", "content": "yes again"})

    assert article.status_code == 200, f"Failed to create article: {article.json()}"

    article_id = article.json()["article_id"]
    admin_client.post(f"/articles/{article_id}/submit")

    return article_id

@pytest.fixture()
def article_approved(admin_token, article_submit):
    admin_client = TestClient(app)
    admin_client.headers.update({"Authorization": f"Bearer {admin_token}"})
    with patch("routers.articles.new_notification", new_callable=AsyncMock):
  
        admin_client.post(f"/articles/{article_submit}/approve")

    return article_submit

