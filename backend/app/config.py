"""Application configuration"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Neon Snake Arena API"
    version: str = "1.0.0"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        # Render deployment - update with your actual URL
        "https://*.onrender.com",
    ]
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./snake_arena.db"
    database_echo: bool = False  # Set to True to log SQL queries
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database"""
        return self.database_url.startswith("sqlite")
    
    @property
    def async_database_url(self) -> str:
        """Get async database URL"""
        # Ensure async drivers are used
        if "postgresql" in self.database_url and "asyncpg" not in self.database_url:
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        if "sqlite" in self.database_url and "aiosqlite" not in self.database_url:
            return self.database_url.replace("sqlite://", "sqlite+aiosqlite://")
        return self.database_url
    
    class Config:
        env_file = ".env"


settings = Settings()
