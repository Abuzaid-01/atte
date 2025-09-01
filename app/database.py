from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Configure connection args based on database type
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif settings.DATABASE_URL.startswith("postgresql"):
    connect_args = {"sslmode": "require"} if "sslmode" not in settings.DATABASE_URL else {}
else:
    connect_args = {}

engine = create_engine(settings.DATABASE_URL, future=True, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
