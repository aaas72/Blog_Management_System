# Blog Management System

A production-ready Backend for a Blog system built with Python, FastAPI, SQLAlchemy, and MySQL.

## Features

- **MVC Architecture**: Clear separation of concerns (Controllers, Services, Repositories).
- **Authentication**: JWT-based auth with Role-Based Access Control (RBAC).
- **Database**: MySQL with SQLAlchemy ORM.
- **Logging**: Professional logging with rotation (Request, App, Error logs).
- **Error Handling**: Global middleware for standardized JSON error responses.
- **Testing**: Ready for high code coverage with `pytest`.

## Requirements

- Python 3.10+
- MySQL 8.0+

## Setup

1. **Clone the repository**:

   ```bash
   git clone <repo_url>
   cd Blog_Management_System
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:

   Navigate to the `blog_system` directory, copy `.env.example` to `.env` and configure your database credentials.

   ```bash
   cd blog_system
   cp .env.example .env
   ```

   Update `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_NAME` in `.env`.

5. **Initialize Database**:
   Make sure MySQL is running and the database `blog_db` exists.
   ```sql
   CREATE DATABASE blog_db;
   ```
   Run the initialization script (make sure you are in `blog_system` directory):
   ```bash
   python database/init_db.py
   ```

## Running the Application

Start the server using Uvicorn (from `blog_system` directory):

```bash
python app.py
```

The API will be available at `http://localhost:8000`.
Interactive API docs: `http://localhost:8000/docs`.

## Running Tests

Run unit and integration tests with coverage:

```bash
# From project root
pytest --cov=blog_system blog_system/tests/
```

## Project Structure

```
.
├── blog_system/
│   ├── app.py              # Application entry point
│   ├── controllers/        # API Routers (Endpoints)
│   ├── services/           # Business Logic
│   ├── repositories/       # Database Access
│   ├── models/             # SQLAlchemy Models
│   ├── schemas/            # Pydantic Models (DTOs)
│   ├── middlewares/        # Custom Middlewares
│   ├── utils/              # Helpers (JWT, Logger, etc.)
│   ├── database/           # DB Connection & Init
│   ├── tests/              # Test Suite
│   └── logs/               # Log files
├── .gitignore
├── requirements.txt
└── README.md
```
