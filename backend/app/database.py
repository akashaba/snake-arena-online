"""Mock database - in-memory storage for development"""
import random
from datetime import datetime, timedelta
from typing import Literal
from app.models import UserInDB, LeaderboardEntryInDB, ActivePlayerInDB
from app.schemas.spectate import Position


class MockDatabase:
    """In-memory database for development"""
    
    def __init__(self):
        self.users: dict[str, UserInDB] = {}
        self.users_by_email: dict[str, str] = {}  # email -> user_id
        self.leaderboard: list[LeaderboardEntryInDB] = []
        self.active_players: dict[str, ActivePlayerInDB] = {}
        self.blacklisted_tokens: set[str] = set()
        
        self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize with mock data matching frontend expectations"""
        import bcrypt
        
        def hash_password(password: str) -> str:
            """Hash a password using bcrypt"""
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        
        # Create mock users - expanded for better testing
        mock_users_data = [
            ("user1", "NeonMaster", "neon@example.com", "password123"),
            ("user2", "CyberSnake", "cyber@example.com", "password123"),
            ("user3", "PixelHunter", "pixel@example.com", "password123"),
            ("user4", "GridRunner", "grid@example.com", "password123"),
            ("user5", "RetroGamer", "retro@example.com", "password123"),
            ("user6", "TronLegend", "tron@example.com", "password123"),
            ("user7", "ArcadeKing", "arcade@example.com", "password123"),
            ("user8", "NeonNinja", "ninja@example.com", "password123"),
            ("user9", "SnakeWizard", "wizard@example.com", "password123"),
            ("user10", "ByteEater", "byte@example.com", "password123"),
            ("user11", "PixelWarrior", "warrior@example.com", "password123"),
            ("user12", "GlowRunner", "glow@example.com", "password123"),
            ("user13", "NeonPhantom", "phantom@example.com", "password123"),
            ("user14", "CyberViper", "viper@example.com", "password123"),
            ("user15", "GridMaster", "gridmaster@example.com", "password123"),
            ("user16", "SnakeKing", "king@example.com", "password123"),
            ("user17", "NeonRacer", "racer@example.com", "password123"),
            ("user18", "PixelNinja", "pixelninja@example.com", "password123"),
            ("user19", "TronWarrior", "tronwar@example.com", "password123"),
            ("user20", "CyberHunter", "hunter@example.com", "password123"),
        ]
        for user_id, username, email, password in mock_users_data:
            user = UserInDB(
                id=user_id,
                username=username,
                email=email,
                hashed_password=hash_password(password),
                created_at=datetime.now() - timedelta(days=random.randint(30, 365))
            )
            self.users[user_id] = user
            self.users_by_email[email] = user_id
        
        # Create mock leaderboard entries - minimal data for testing
        mock_leaderboard_data = [
            # Just a few top scores so user can see their score on the leaderboard
            ("user1", "NeonMaster", 450, "walls"),
            ("user16", "SnakeKing", 380, "pass-through"),
            ("user2", "CyberSnake", 320, "walls"),
            ("user15", "GridMaster", 280, "pass-through"),
            ("user3", "PixelHunter", 240, "walls"),
        ]
        
        for idx, (user_id, username, score, mode) in enumerate(mock_leaderboard_data):
            entry = LeaderboardEntryInDB(
                id=f"entry{idx + 1}",
                user_id=user_id,
                username=username,
                score=score,
                mode=mode,  # type: ignore
                timestamp=datetime.now() - timedelta(hours=idx + 1)
            )
            self.leaderboard.append(entry)
        
        # Create mock active players
        self._create_mock_active_players()
    
    def _generate_mock_snake(self) -> list[Position]:
        """Generate a mock snake"""
        length = random.randint(3, 8)
        start_x = random.randint(length, 19)  # Ensure enough space for snake
        start_y = random.randint(3, 16)
        
        snake = [Position(x=start_x, y=start_y)]
        for i in range(1, length):
            # Build snake to the left
            x = max(0, start_x - i)  # Prevent going negative
            snake.append(Position(x=x, y=start_y))
        
        return snake
    
    def _create_mock_active_players(self):
        """Create mock active players for spectate mode"""
        mock_active = [
            ("p1", "user1", "NeonMaster", 430, "walls"),
            ("p2", "user2", "CyberSnake", 380, "pass-through"),
            ("p3", "user3", "PixelHunter", 350, "walls"),
            ("p4", "user16", "SnakeKing", 320, "pass-through"),
            ("p5", "user9", "SnakeWizard", 290, "walls"),
            ("p6", "user15", "GridMaster", 260, "pass-through"),
            ("p7", "user17", "NeonRacer", 230, "walls"),
            ("p8", "user10", "ByteEater", 200, "pass-through"),
            ("p9", "user4", "GridRunner", 180, "walls"),
            ("p10", "user14", "CyberViper", 150, "pass-through"),
        ]
        
        for player_id, user_id, username, score, mode in mock_active:
            player = ActivePlayerInDB(
                id=player_id,
                username=username,
                score=score,
                mode=mode,  # type: ignore
                snake=self._generate_mock_snake(),
                food=Position(
                    x=random.randint(0, 19),
                    y=random.randint(0, 19)
                ),
                is_game_over=False,
                direction=random.choice(["UP", "DOWN", "LEFT", "RIGHT"]),  # type: ignore
                started_at=datetime.now() - timedelta(minutes=random.randint(1, 30))
            )
            self.active_players[player_id] = player
    
    # User operations
    def get_user_by_id(self, user_id: str) -> UserInDB | None:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> UserInDB | None:
        """Get user by email"""
        user_id = self.users_by_email.get(email)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def create_user(self, user: UserInDB) -> UserInDB:
        """Create a new user"""
        self.users[user.id] = user
        self.users_by_email[user.email] = user.id
        return user
    
    # Leaderboard operations
    def get_leaderboard(
        self,
        mode: Literal["walls", "pass-through"] | None = None,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[list[LeaderboardEntryInDB], int]:
        """Get leaderboard with filtering and pagination"""
        entries = self.leaderboard
        
        if mode:
            entries = [e for e in entries if e.mode == mode]
        
        # Sort by score descending
        entries = sorted(entries, key=lambda x: (-x.score, x.timestamp))
        
        total = len(entries)
        paginated = entries[offset:offset + limit]
        
        return paginated, total
    
    def get_user_scores(
        self,
        user_id: str,
        mode: Literal["walls", "pass-through"] | None = None
    ) -> list[LeaderboardEntryInDB]:
        """Get all scores for a user"""
        entries = [e for e in self.leaderboard if e.user_id == user_id]
        
        if mode:
            entries = [e for e in entries if e.mode == mode]
        
        return sorted(entries, key=lambda x: (-x.score, x.timestamp))
    
    def add_score(self, entry: LeaderboardEntryInDB) -> LeaderboardEntryInDB:
        """Add a new score to leaderboard"""
        self.leaderboard.append(entry)
        return entry
    
    # Spectate operations
    def get_active_players(
        self,
        mode: Literal["walls", "pass-through"] | None = None
    ) -> list[ActivePlayerInDB]:
        """Get all active players"""
        players = list(self.active_players.values())
        
        if mode:
            players = [p for p in players if p.mode == mode]
        
        # Filter out game over players
        players = [p for p in players if not p.is_game_over]
        
        # Simulate movement by regenerating snake positions
        for player in players:
            player.snake = self._generate_mock_snake()
            player.score += random.randint(0, 20)
        
        return players
    
    def get_active_player(self, player_id: str) -> ActivePlayerInDB | None:
        """Get a specific active player"""
        player = self.active_players.get(player_id)
        
        if player and not player.is_game_over:
            # Simulate movement
            player.snake = self._generate_mock_snake()
            player.score += random.randint(0, 20)
            return player
        
        return None
    
    # Token blacklist operations
    def blacklist_token(self, token: str):
        """Add token to blacklist"""
        self.blacklisted_tokens.add(token)
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""
        return token in self.blacklisted_tokens


# Global database instance
db = MockDatabase()
