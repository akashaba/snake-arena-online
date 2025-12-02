"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from app.database import db, MockDatabase
from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def reset_db():
    """Reset database before each test"""
    # Save the current db
    global db
    # Create a fresh database
    db.__init__()
    yield
    # Database will be reset for next test


@pytest.fixture
def auth_token(client, reset_db):
    """Get authentication token for testing"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "neon@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    """Get authentication headers"""
    return {"Authorization": f"Bearer {auth_token}"}
