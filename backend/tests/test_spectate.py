"""Tests for spectate endpoints"""
import pytest


class TestSpectate:
    """Test spectate endpoints"""
    
    def test_get_active_players(self, client, reset_db):
        """Test getting active players"""
        response = client.get("/api/v1/spectate/players")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check structure of player data
        player = data[0]
        assert "id" in player
        assert "username" in player
        assert "score" in player
        assert "mode" in player
        assert "snake" in player
        assert "food" in player
        assert "is_game_over" in player
    
    def test_get_active_players_with_mode_filter(self, client, reset_db):
        """Test getting active players filtered by mode"""
        response = client.get("/api/v1/spectate/players?mode=walls")
        
        assert response.status_code == 200
        data = response.json()
        assert all(player["mode"] == "walls" for player in data)
    
    def test_watch_player(self, client, reset_db):
        """Test watching a specific player"""
        response = client.get("/api/v1/spectate/players/p1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "p1"
        assert "snake" in data
        assert "food" in data
        assert isinstance(data["snake"], list)
        
        # Verify snake positions have x and y
        for position in data["snake"]:
            assert "x" in position
            assert "y" in position
            assert 0 <= position["x"] <= 19
            assert 0 <= position["y"] <= 19
    
    def test_watch_nonexistent_player(self, client, reset_db):
        """Test watching nonexistent player"""
        response = client.get("/api/v1/spectate/players/nonexistent")
        
        assert response.status_code == 404
    
    def test_snake_structure(self, client, reset_db):
        """Test that snake data structure is correct"""
        response = client.get("/api/v1/spectate/players/p1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Snake should be a list of positions
        assert len(data["snake"]) >= 3  # At least 3 segments
        
        # Food should be a valid position
        assert 0 <= data["food"]["x"] <= 19
        assert 0 <= data["food"]["y"] <= 19
