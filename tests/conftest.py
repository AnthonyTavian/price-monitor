import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.utils.security import get_password_hash
from unittest.mock import AsyncMock, patch

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    user = User(
         email="test@test.com",
        full_name="Test User",
        hashed_password=get_password_hash("test123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def user_token(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "test123"}
    )
    return response.json()["access_token"]

@pytest.fixture(autouse=False)
def mock_scraping():
    with patch('app.services.product_service.scrape_amazon_price', new_callable=AsyncMock) as mock:
        mock.return_value = {"price": 1000.0, "name": "Test Product"}
        yield mock

@pytest.fixture(scope="function")
def products_data(client, user_token, mock_scraping):
    mock_scraping.return_value = {"price": 1000.0, "name": "Test Product"}
    
    response = client.post(
        "/products",
        json={"url": "https://www.amazon.com.br/dp/123", "target_price": 900.0},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    return [response.json()]