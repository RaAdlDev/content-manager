# Content Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A REST API for content management built with **FastAPI** and **SQLAlchemy 2.0**. Specs: tests with pytests, user authentication with JWT, roles system, clean architecture and a sistem of notifications with WebSockets.

---

##  Project Structure

```
CONTENT/
├── core/
│   ├── security.py       # JWT, password hashing, auth dependencies
│   └── settings.py       # Environment-based configuration
├── database/
│   ├── connection.py     # SQLAlchemy engine and session 
├── dependencies/
│   ├── auth.py           # Auth dependences
│   └── roles.py          # Roles dependences  
├── models/               # ORM models         
│   ├── all_tables.py       
│   ├── article_tag.py    # Many to many relationship
│   ├── article.py        # Article models
│   ├── base.py           
│   ├── category.py       # Category models
│   ├── notification.py   # Notification models
│   ├── tag.py            # Tag models
│   └── user.py           # User models
├── routers/
│   ├── articles.py       # Articles endpoints
│   ├── auth.py           # Auth endpoints        
│   └── websocket.py      # Websocket handshake and functions manager
├── schemas/
│   ├── article.py        # Article input, pagination, output and update schema
│   ├── notification.py   # Token input and output
│   ├── rejection.py      # Rejection input 
│   ├── token.py          # Token output
│   └── user.py           # User input and output
├── services/
│   ├── articles_services.py        # Articles logic
│   ├── auth_services.py            # Auth logic
│   ├── category_services.py        # Category logic
│   ├── notification_services.py    # Notification logic
│   └── tags_services.py            # Tags logic
├── tests/
│   ├── conftest.py        # Test fixtures
│   ├── test_articles.py   # Articles tests logic
│   ├── test_auth.py       # Auth tests logic
│   ├── test_category.py   # Category tests logic
│   ├── test_roles.py      # Roles tests logic
│   └── test_tag.py        # Tag tests logic
├── .env.example
├── main.py
└── requirements.txt
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/RaAdlDev/content-manager.git
cd content-manager
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DE_DATOS
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
TOKEN_DURATION=60
TESTING_DATABASE_URL=postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DE_DATOS

```

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy DB URL | `postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DE_DATOS` |
| `SECRET_KEY` | JWT signing key | `mysecretkey123` 
| `ALGORITHM` | JWT algorithm | `HS256` |
| `TOKEN_DURATION` | Token expiry in minutes | `60` |
| `TESTING_DATABASE_URL` | Testing SQLAlchemy DB URL | `postgresql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BASE_DE_DATOS` |


### 5. Upgrade tables

```bash
alembic upgrade head
```

---

### 6. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## 🔐 Authentication



### Login

```http
POST /auth/login

{
  "email": "example@example.com",
  "password": "Secret123*"
}
```

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests:

```http
Authorization: Bearer <your_token>
```

---

## 📋 Endpoints

### 👤 Auth

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `POST` | `/auth/register` | Register a new user ||
| `POST` | `/auth/login` | Login and get JWT token ||
| `PATCH` | `/auth/{user_id}/deactivate` | Deactivate a user | ADMIN |
| `PATCH` | `/auth/{user_id}/writer` | Reader to writer | ADMIN |
| `PATCH` | `/auth/{user_id}/admin` | Reader or writer to admin | ADMIN |


#### Register a user
```http
POST /auth/register
Content-Type: application/json

{
  "email": "example@example.com",
  "password": "Securepass123*"
}
```



---

### Articles

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `POST` | `/articles/` | Make an article | ADMIN & WRITER |
| `GET` | `/articles/` | Get articles with pagination |READER, ADMIN & WRITER |
| `GET` | `/my-articles/` | Get all your articles | ADMIN & WRITER |
| `GET` | `/articles/{article_id}` | Get an article | READER, ADMIN & WRITER |
| `PATCH` | `/articles/{article_id}` | Edit an article | ADMIN & WRITER |
| `POST` | `/articles/{article_id}/submit` | Submit an article for review | ADMIN & WRITER |
| `POST` | `/articles/{article_id}/approve` | Approve an article | ADMIN |
| `POST` | `/articles/{article_id}/reject` | Reject an article | ADMIN |
| `DELETE` | `/articles/{article_id}/delete` | Delete an article | ADMIN |



### Categories

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `POST` | `/category/` | Make a category | ADMIN |
| `GET` | `/category/` | Get all the categories | |

### Tags

| Method | Endpoint | Description | Role |
|---|---|---|---|
| `POST` | `/tag/` | Make a tag | ADMIN |
| `GET` | `/tag/` | Get all the tags | |




### Websocket

| Method | Endpoint | Description |
|---|---|---|
| `WEBSOCKET` | `/ws` | Make a connection to recive notifications |

If someone sends you a notification when you are offline, the database will save it for you and send it when you are back online.

## Pytests

To make de project more scalable, eficient and clean, tests have been implemented. The auth, the articles manager and the roles had their own tests. Before running tests, create a new database only for tests in PostgresSQL called "content_api_test"


### Run the tests

```bash
pytest tests/ -v
```


## 🗄️ Database Models

```
User
├── user_id (PK, UUID)
├── email (unique)
├── hashed_password 
├── role (READER|WRITER|ADMIN)
├── is_active (bool)
├── created_at (datetime)
└── user_articles → Article (1:N)

Article
├── article_id (PK, UUID)
├── author_id (ForeignKey)
├── category_id (ForeignKey, nullable)
├── title 
├── content
├── status (DRAFT|PENDING_REVIEW|PUBLISHED|REJECTED)
├── rejection_reason (nullable)
├── created_at (datetime)
├── updated_at (datetime, nullable)
├── deleted_at (datetime, nullable)
├── tags → Tag (N:M)
└── user → User (N:1)

article_tag
├── article_id (ForeignKey, PK)
└── tag_id (ForeignKey, PK)

Tag
├── tag_id (PK, UUID)
├── name (unique)
├── slug (unque)
└── articles → Article (N:M)

Category
├── category_id (PK, UUID)
├── name (unique)
└── slug (unique)

Notification
├── notification_id (PK, UUID)
├── user_id (ForeignKey)
├── article_id (ForeignKey)
├── message 
├── is_read (bool)
└── created_at (datetime)

```

---

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | ORM |
| [PostgreSQL](https://www.postgresql.org/) | Relational database management system |
| [Alembic](https://alembic.sqlalchemy.org/) | Database migrations management |
| [psycopg2](https://www.psycopg.org/) | PostgreSQL database adapter for Python |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation |
| [python-jose](https://github.com/mpdavis/python-jose) | JWT tokens |
| [passlib](https://passlib.readthedocs.io/) | Password hashing (bcrypt) |

---

## 📄 License

MIT License. Feel free to use and modify this project.