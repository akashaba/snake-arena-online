"""Integration tests for authentication endpoints"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_signup_and_login(client: AsyncClient, db_session: AsyncSession):
    """Test user signup and login flow"""
    # Signup
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["username"] == "testuser"
    signup_token = data["token"]

    # Login with same credentials
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient, db_session: AsyncSession):
    """Test that duplicate email returns conflict error"""
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }

    # First signup
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 201

    # Try to signup again with same email
    signup_data["username"] = "anotheruser"
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, db_session: AsyncSession):
    """Test login with invalid credentials"""
    # Try to login without signing up
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, db_session: AsyncSession):
    """Test getting current user information"""
    # Signup first
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    token = response.json()["token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, db_session: AsyncSession):
    """Test logout functionality"""
    # Signup
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    response = await client.post("/api/v1/auth/signup", json=signup_data)
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Verify token works
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200

    # Logout
    response = await client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 200

    # Verify token is blacklisted
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient, db_session: AsyncSession):
    """Test that protected routes require authentication"""
    # Try to access protected endpoint without token
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401  # 401 for missing auth

    # Try with invalid token
    headers = {"Authorization": "Bearer invalidtoken"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401
