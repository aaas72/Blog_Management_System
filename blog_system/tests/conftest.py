import pytest
import os
import sys
import warnings

# Suppress DeprecationWarning from httpx used by TestClient
warnings.filterwarnings("ignore", message="The 'app' shortcut is now deprecated")

# Add blog_system directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load env before importing app
load_dotenv()

from app import app
from database.db import Base, get_db
from utils.password_utils import get_password_hash
from models.user_model import User, UserRole

# Load environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
TEST_DB_NAME = "blog_test_db"

# Construct the database URL for MySQL Test DB
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

# Create engine for test database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create tables at the start of the test session and drop them at the end.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database session for each test.
    Clean up data before/after.
    """
    # Create session
    session = TestingSessionLocal()
    
    # Truncate/Clean tables (disable FK checks for MySQL)
    # Using delete() instead of TRUNCATE to avoid "Table definition has changed" errors in some MySQL versions/configs during transactions
    session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    session.commit()

    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db):
    """
    Test client that overrides the get_db dependency.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def admin_token(client, db):
    """
    Create an admin user and return their token.
    """
    admin = User(
        username="admin_test",
        password_hash=get_password_hash("Admin@123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    
    response = client.post("/api/auth/login", json={"username": "admin_test", "password": "Admin@123"})
    return response.json()["data"]["access_token"]

@pytest.fixture(scope="function")
def author_token(client, db):
    """
    Create an author user and return their token.
    """
    author = User(
        username="author_test",
        password_hash=get_password_hash("Author@123"),
        role=UserRole.AUTHOR,
        is_active=True
    )
    db.add(author)
    db.commit()
    
    response = client.post("/api/auth/login", json={"username": "author_test", "password": "Author@123"})
    return response.json()["data"]["access_token"]

@pytest.fixture(scope="function")
def reader_token(client, db):
    """
    Create a reader user and return their token.
    """
    reader = User(
        username="reader_test",
        password_hash=get_password_hash("Reader@123"),
        role=UserRole.READER,
        is_active=True
    )
    db.add(reader)
    db.commit()
    
    response = client.post("/api/auth/login", json={"username": "reader_test", "password": "Reader@123"})
    return response.json()["data"]["access_token"]
