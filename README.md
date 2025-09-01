# 🎓 Attendance System Backend API

A modern FastAPI-based backend for managing school attendance with JWT authentication, PostgreSQL database support, and comprehensive CRUD operations.

## 🚀 **Features**

- **FastAPI Framework** - High-performance, modern Python web framework
- **JWT Authentication** - Secure token-based user authentication
- **PostgreSQL Support** - Production-ready database with SQLAlchemy ORM
- **CRUD Operations** - Complete management of classes, students, and attendance
- **Email Integration** - Optional email notifications
- **CORS Enabled** - Cross-origin resource sharing for frontend integration
- **Auto Documentation** - Swagger/OpenAPI docs at `/docs`

## 📋 **API Endpoints**

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Classes Management
- `GET /classes/` - List all classes
- `POST /classes/` - Create new class
- `PUT /classes/{id}` - Update class
- `DELETE /classes/{id}` - Delete class

### Students Management
- `GET /students/{class_id}` - Get students in a class
- `POST /students/` - Add new student
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Attendance Management
- `GET /attendance/{class_id}` - Get attendance records
- `POST /attendance/` - Mark attendance
- `GET /attendance/{class_id}/summary` - Get attendance summary

## 🛠 **Tech Stack**

- **FastAPI** 0.110.0 - Web framework
- **SQLAlchemy** 2.0.29 - ORM
- **PostgreSQL** - Production database
- **Python-JOSE** - JWT handling
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 🌐 **Deployment**

This backend is configured for deployment on **Render** with:
- `Procfile` - Web service configuration
- `render.yaml` - Infrastructure as code
- `runtime.txt` - Python version specification
- Environment variable support
- PostgreSQL database integration

## 🔧 **Environment Variables**

```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-super-secret-jwt-key
CORS_ORIGINS=["http://localhost:8501","https://your-frontend.com"]
```

## 📚 **API Documentation**

Once deployed, visit:
- **Swagger UI**: `https://your-backend.onrender.com/docs`
- **ReDoc**: `https://your-backend.onrender.com/redoc`

## 🔗 **Frontend Integration**

This backend is designed to work with the FastAPI frontend component. Update your frontend's API_URL to point to the deployed backend:

```python
API_URL = "https://your-backend.onrender.com"
```

## 🛡 **Security Features**

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention via SQLAlchemy
- Environment variable configuration

---

**Built with ❤️ for modern education management**
