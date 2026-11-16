# Blog Management System

A layered REST API for running a multi-author blog: role-based permissions, a full post lifecycle (draft → published → archived → restored), an audit trail of every change, and an automated test suite.

![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Features

- **Authentication** — registration and login with JWT access tokens and bcrypt-hashed passwords
- **Role-based access control** — three roles with clear rules:

  | Role | Permissions |
  |---|---|
  | `admin` | Manage every post |
  | `author` | Create posts and manage only their own |
  | `reader` | Read published content |

- **Post lifecycle** — posts start as drafts and move through publish, archive and restore actions
- **Audit trail** — every significant action is recorded with the user, entity and details
- **Consistent errors** — global exception handlers return standardized JSON error responses
- **Tested** — unit and integration tests for auth, security, posts, workflow and auditing

## Architecture

Requests flow through clearly separated layers:

```text
controllers (FastAPI routers)
      │  validate input with Pydantic schemas
      ▼
services (business rules, permissions, audit logging)
      │
      ▼
repositories (data access) ─▶ SQLAlchemy models ─▶ MySQL
```

```text
blog_system/
├── app.py            # Application entry point
├── controllers/      # auth_controller, post_controller
├── services/         # auth, post, audit services
├── repositories/     # user, post, audit repositories
├── models/           # User, Post, AuditLog
├── schemas/          # Pydantic request/response models
├── middlewares/      # Auth dependency, global error handlers
├── utils/            # JWT, password hashing, exceptions, responses
├── database/         # Connection and init script
└── tests/            # pytest suite
```

## API Overview

All routes are served under `/api`. Interactive documentation is available at `/docs`.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Create an account |
| `POST` | `/api/auth/login` | Get an access token |
| `GET` | `/api/auth/me` | Current user |
| `GET` | `/api/posts` | List posts |
| `POST` | `/api/posts` | Create a post (admin, author) |
| `GET` | `/api/posts/mine` | Current user's posts |
| `GET` | `/api/posts/{id}` | Get a post |
| `PUT` | `/api/posts/{id}` | Update a post |
| `POST` | `/api/posts/{id}/publish` | Publish |
| `POST` | `/api/posts/{id}/archive` | Archive |
| `POST` | `/api/posts/{id}/restore` | Restore |
| `DELETE` | `/api/posts/{id}` | Delete |

## Getting Started

**Requirements:** Python 3.10+, MySQL 8

```bash
git clone https://github.com/aaas72/Blog_Management_System.git
cd Blog_Management_System
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `blog_system/.env`:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=blog_db
JWT_SECRET=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Create the database and tables, then start the server:

```bash
mysql -u root -p -e "CREATE DATABASE blog_db"
cd blog_system
python database/init_db.py
python app.py                     # http://localhost:8000/docs
```

## Running Tests

```bash
pytest --cov=blog_system blog_system/tests/
```

## Author

**Abdellah Sheikh** — [abdellahsheikh.dev](https://abdellahsheikh.dev) · [LinkedIn](https://www.linkedin.com/in/abdellahsheikh)

Licensed under the [MIT License](LICENSE).
