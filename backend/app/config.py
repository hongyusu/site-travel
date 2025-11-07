"""Application configuration."""

from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import os
from pathlib import Path

# Get the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "FindTravelMate"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/findtravelmate"
    DATABASE_ECHO: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # File Upload
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Commission
    DEFAULT_COMMISSION_RATE: float = 20.0

    # Booking
    FREE_CANCELLATION_HOURS: int = 24
    DEFAULT_CURRENCY: str = "EUR"

    # Email
    RESEND_API_KEY: str = "re_W314AQWC_AWo6mye59GD11pSfZ8533yG4"
    EMAIL_FROM: str = "onboarding@resend.dev"  # Use verified domain for testing
    EMAIL_FROM_NAME: str = "FindTravelMate"
    EMAIL_ENABLED: bool = True  # Enable for testing with verified email
    EMAIL_TESTING_MODE: bool = True  # Redirect all emails to verified address
    EMAIL_TEST_RECIPIENT: str = "hongyu.su.uh@gmail.com"  # Your verified email

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()