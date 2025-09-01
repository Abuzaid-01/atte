
# from pydantic_settings import BaseSettings
# from pydantic import EmailStr

# class Settings(BaseSettings):
#     DATABASE_URL: str = "sqlite:///./attendance.db"
#     JWT_SECRET: str = "change-me"
#     JWT_ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
#     CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

#     # optional mail
#     MAIL_USERNAME: str | None = None
#     MAIL_PASSWORD: str | None = None
#     MAIL_FROM: EmailStr | None = None
#     MAIL_SERVER: str | None = None
#     MAIL_PORT: int | None = 587
#     MAIL_TLS: bool = True
#     MAIL_SSL: bool = False

#     class Config:
#         env_file = ".env"


# settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    # For Render, use environment variable
    DATABASE_URL: str = "sqlite:///./attendance.db"  # Local development
    # DATABASE_URL will be overridden by Render's environment variable
    
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "https://*.onrender.com"
    ]

    # Mail settings
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: EmailStr | None = None
    MAIL_SERVER: str | None = None
    MAIL_PORT: int | None = 587
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        env_file = ".env"

settings = Settings()