"""Tests for authentication endpoints"""
import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "neon@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == "neon@example.com"
        assert data["user"]["username"] == "NeonMaster"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "neon@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
    
    def test_signup_success(self, client):
        """Test successful signup"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "NewPlayer",
                "email": "newplayer@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == "newplayer@example.com"
        assert data["user"]["username"] == "NewPlayer"
    
    def test_signup_duplicate_email(self, client):
        """Test signup with duplicate email"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "NewPlayer",
                "email": "neon@example.com",  # Existing email
                "password": "password123"
            }
        )
        
        assert response.status_code == 409
    
    def test_signup_invalid_username(self, client):
        """Test signup with invalid username"""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "ab",  # Too short
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 422
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user"""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "NeonMaster"
        assert data["email"] == "neon@example.com"
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_logout(self, client, auth_headers):
        """Test logout"""
        response = client.post(
            "/api/v1/auth/logout",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"
        
        # Token should be blacklisted
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        assert response.status_code == 401
