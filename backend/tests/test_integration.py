"""Integration tests for the API"""
import pytest


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_user_flow(self, client):
        """Test complete user flow: signup, login, submit score, view profile"""
        # 1. Signup
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "TestPlayer",
                "email": "testplayer@example.com",
                "password": "testpass123"
            }
        )
        assert signup_response.status_code == 201
        token = signup_response.json()["token"]
        user_id = signup_response.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Submit a score
        score_response = client.post(
            "/api/v1/leaderboard/scores",
            headers=headers,
            json={
                "score": 350,
                "mode": "walls"
            }
        )
        assert score_response.status_code == 201
        
        # 3. View profile
        profile_response = client.get(f"/api/v1/users/{user_id}")
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["total_games"] == 1
        assert profile_data["highest_score"] == 350
        
        # 4. View stats
        stats_response = client.get(f"/api/v1/users/{user_id}/stats")
        assert stats_response.status_code == 200
        stats_data = stats_response.json()
        assert stats_data["total_games"] == 1
        assert stats_data["total_score"] == 350
        assert stats_data["wall_mode_games"] == 1
        
        # 5. Logout
        logout_response = client.post(
            "/api/v1/auth/logout",
            headers=headers
        )
        assert logout_response.status_code == 200
    
    def test_leaderboard_ranking(self, client, auth_headers):
        """Test that leaderboard ranking works correctly"""
        # Submit multiple scores
        scores = [100, 300, 200, 500, 150]
        
        for score in scores:
            response = client.post(
                "/api/v1/leaderboard/scores",
                headers=auth_headers,
                json={
                    "score": score,
                    "mode": "walls"
                }
            )
            assert response.status_code == 201
        
        # Get leaderboard
        response = client.get("/api/v1/leaderboard?mode=walls")
        assert response.status_code == 200
        
        entries = response.json()["entries"]
        scores_list = [entry["score"] for entry in entries]
        
        # Verify scores are in descending order
        assert scores_list == sorted(scores_list, reverse=True)
    
    def test_spectate_workflow(self, client):
        """Test spectate workflow"""
        # 1. Get all active players
        players_response = client.get("/api/v1/spectate/players")
        assert players_response.status_code == 200
        players = players_response.json()
        assert len(players) > 0
        
        # 2. Watch a specific player
        player_id = players[0]["id"]
        watch_response = client.get(f"/api/v1/spectate/players/{player_id}")
        assert watch_response.status_code == 200
        
        player_data = watch_response.json()
        assert player_data["id"] == player_id
        assert len(player_data["snake"]) >= 3
    
    def test_api_root_and_health(self, client):
        """Test root and health endpoints"""
        root_response = client.get("/")
        assert root_response.status_code == 200
        assert "message" in root_response.json()
        
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
