from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "sqlite:///./attendance.db"  
    
    # JWT Configuration
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days = 43,200 minutes
    
    # CORS Origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "https://*.onrender.com"
    ]

    # Mail settings (optional)
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
