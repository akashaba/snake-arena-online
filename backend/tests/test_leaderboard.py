"""Tests for leaderboard endpoints"""
import pytest


class TestLeaderboard:
    """Test leaderboard endpoints"""
    
    def test_get_leaderboard(self, client, reset_db):
        """Test getting leaderboard"""
        response = client.get("/api/v1/leaderboard")
        
        assert response.status_code == 200
        data = response.json()
        assert "entries" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert len(data["entries"]) > 0
    
    def test_get_leaderboard_with_mode_filter(self, client, reset_db):
        """Test getting leaderboard filtered by mode"""
        response = client.get("/api/v1/leaderboard?mode=walls")
        
        assert response.status_code == 200
        data = response.json()
        assert all(entry["mode"] == "walls" for entry in data["entries"])
    
    def test_get_leaderboard_with_pagination(self, client, reset_db):
        """Test leaderboard pagination"""
        response = client.get("/api/v1/leaderboard?limit=5&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 0
        assert len(data["entries"]) <= 5
    
    def test_get_top_scores(self, client, reset_db):
        """Test getting top scores"""
        response = client.get("/api/v1/leaderboard/top?limit=3")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
        # Verify scores are sorted descending
        scores = [entry["score"] for entry in data]
        assert scores == sorted(scores, reverse=True)
    
    def test_submit_score(self, client, reset_db, auth_headers):
        """Test submitting a score"""
        response = client.post(
            "/api/v1/leaderboard/scores",
            headers=auth_headers,
            json={
                "score": 500,
                "mode": "walls"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 500
        assert data["mode"] == "walls"
        assert data["username"] == "NeonMaster"
    
    def test_submit_score_unauthorized(self, client, reset_db):
        """Test submitting score without authentication"""
        response = client.post(
            "/api/v1/leaderboard/scores",
            json={
                "score": 500,
                "mode": "walls"
            }
        )
        
        assert response.status_code == 401
    
    def test_submit_score_invalid_mode(self, client, reset_db, auth_headers):
        """Test submitting score with invalid mode"""
        response = client.post(
            "/api/v1/leaderboard/scores",
            headers=auth_headers,
            json={
                "score": 500,
                "mode": "invalid-mode"
            }
        )
        
        assert response.status_code == 422
    
    def test_get_user_scores(self, client, reset_db):
        """Test getting user scores"""
        response = client.get("/api/v1/leaderboard/user/user1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(entry["user_id"] == "user1" for entry in data)
    
    def test_get_user_scores_nonexistent(self, client, reset_db):
        """Test getting scores for nonexistent user"""
        response = client.get("/api/v1/leaderboard/user/nonexistent")
        
        assert response.status_code == 404
