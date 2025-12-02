"""Data migration script to populate database with test data"""
import asyncio
import random
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt

from app.config import settings
from app.crud import active_players, leaderboard, users
from app.database import AsyncSessionLocal, init_db


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def generate_mock_snake() -> list[dict]:
    """Generate a mock snake"""
    length = random.randint(3, 8)
    start_x = random.randint(length, 19)
    start_y = random.randint(3, 16)

    snake = [{"x": start_x, "y": start_y}]
    for i in range(1, length):
        x = max(0, start_x - i)
        snake.append({"x": x, "y": start_y})

    return snake


async def populate_database():
    """Populate database with test data"""
    print("Initializing database...")
    await init_db()

    async with AsyncSessionLocal() as db:
        print("Creating users...")
        # Create mock users
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
            await users.create_user(
                db,
                user_id=user_id,
                username=username,
                email=email,
                hashed_password=hash_password(password),
            )
        print(f"Created {len(mock_users_data)} users")

        print("Creating leaderboard entries...")
        # Create mock leaderboard entries
        mock_leaderboard_data = [
            ("user1", "NeonMaster", 450, "walls"),
            ("user16", "SnakeKing", 380, "pass-through"),
            ("user2", "CyberSnake", 320, "walls"),
            ("user15", "GridMaster", 280, "pass-through"),
            ("user3", "PixelHunter", 240, "walls"),
        ]

        for idx, (user_id, username, score, mode) in enumerate(mock_leaderboard_data):
            await leaderboard.add_score(
                db,
                user_id=user_id,
                username=username,
                score=score,
                mode=mode,
            )
        print(f"Created {len(mock_leaderboard_data)} leaderboard entries")

        print("Creating active players...")
        # Create mock active players
        mock_active = [
            ("p1", "NeonMaster", 430, "walls"),
            ("p2", "CyberSnake", 380, "pass-through"),
            ("p3", "PixelHunter", 350, "walls"),
            ("p4", "SnakeKing", 320, "pass-through"),
            ("p5", "SnakeWizard", 290, "walls"),
            ("p6", "GridMaster", 260, "pass-through"),
            ("p7", "NeonRacer", 230, "walls"),
            ("p8", "ByteEater", 200, "pass-through"),
            ("p9", "GridRunner", 180, "walls"),
            ("p10", "CyberViper", 150, "pass-through"),
        ]

        for player_id, username, score, mode in mock_active:
            snake = generate_mock_snake()
            food = {"x": random.randint(0, 19), "y": random.randint(0, 19)}
            direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

            await active_players.create_active_player(
                db,
                player_id=player_id,
                username=username,
                mode=mode,
                snake=snake,
                food=food,
                direction=direction,
            )
            # Update score
            await active_players.update_player_state(
                db,
                player_id=player_id,
                score=score,
            )
        print(f"Created {len(mock_active)} active players")

    print("Database populated successfully!")


if __name__ == "__main__":
    asyncio.run(populate_database())
