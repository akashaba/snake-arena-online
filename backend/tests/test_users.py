"""Tests for user profile endpoints"""
import pytest


class TestUsers:
    """Test user profile endpoints"""
    
    def test_get_user_profile(self, client):
        """Test getting user profile"""
        response = client.get("/api/v1/users/user1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "user1"
        assert data["username"] == "NeonMaster"
        assert "created_at" in data
        assert "total_games" in data
        assert "highest_score" in data
    
    def test_get_user_profile_nonexistent(self, client):
        """Test getting nonexistent user profile"""
        response = client.get("/api/v1/users/nonexistent")
        
        assert response.status_code == 404
    
    def test_get_user_stats(self, client):
        """Test getting user statistics"""
        response = client.get("/api/v1/users/user1/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_games" in data
        assert "total_score" in data
        assert "average_score" in data
        assert "highest_score" in data
        assert "wall_mode_games" in data
        assert "pass_through_mode_games" in data
        assert "best_wall_score" in data
        assert "best_pass_through_score" in data
        assert "rank" in data
        
        # Verify calculations
        assert data["total_games"] >= 0
        assert data["total_score"] >= 0
        assert data["average_score"] >= 0
    
    def test_get_user_stats_nonexistent(self, client):
        """Test getting stats for nonexistent user"""
        response = client.get("/api/v1/users/nonexistent/stats")
        
        assert response.status_code == 404
    
    def test_user_rank_calculation(self, client):
        """Test that user rank is calculated correctly"""
        response = client.get("/api/v1/users/user1/stats")
        
        assert response.status_code == 200
        data = response.json()
        
        # user1 (NeonMaster) has the highest score (850), so rank should be 1
        assert data["rank"] == 1
