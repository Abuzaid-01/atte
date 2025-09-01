# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .config import settings
# from .database import Base, engine
# from .auth.routes import router as auth_router
# from .routes.classes import router as classes_router
# from .routes.students import router as students_router
# from .routes.attendance import router as attendance_router

# # Dev only: auto create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Attendance API", version="0.1.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(classes_router, prefix="/classes", tags=["classes"])
# app.include_router(students_router, prefix="/students", tags=["students"])
# app.include_router(attendance_router, prefix="/attendance", tags=["attendance"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .auth.routes import router as auth_router
from .routes.classes import router as classes_router
from .routes.students import router as students_router
from .routes.attendance import router as attendance_router
import os

# Only create tables in development
if not os.getenv("DATABASE_URL") or "sqlite" in os.getenv("DATABASE_URL", ""):
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance API", version="0.1.0")

# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(classes_router, prefix="/classes", tags=["classes"])
app.include_router(students_router, prefix="/students", tags=["students"])
app.include_router(attendance_router, prefix="/attendance", tags=["attendance"])

@app.get("/")
def root():
    return {"message": "Attendance API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}