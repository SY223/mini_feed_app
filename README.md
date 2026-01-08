

# 📘 **Mini Social Media Feed API — FastAPI Backend**

A modular, secure, and scalable **social media backend API** built with **FastAPI**, featuring JWT authentication, refresh tokens, clean schema separation, and a beginner‑friendly architecture that mirrors real‑world backend engineering practices.

This project is ideal for learning authentication, API design, and backend architecture using modern Python tooling.

---

## 🚀 **Features**

### 🔐 **Authentication**
- User registration  
- Login with username or email  
- Secure password hashing (`pwdlib`)  
- Access tokens (short‑lived)  
- Refresh tokens (long‑lived)  
- Token revocation (logout)  
- `/me` endpoint for authenticated user retrieval  

### 🧱 **Architecture**
- Modular router structure  
- Clean Pydantic schema separation (`UserCreate`, `UserPublic`, `UserInDB`)  
- UUID4 user IDs  
- In‑memory database (easy to replace with PostgreSQL later)  
- Environment‑based configuration  

---

## 🛠 **Tech Stack**

| Component | Technology |
|----------|------------|
| Backend Framework | FastAPI |
| Authentication | OAuth2 + JWT |
| Password Hashing | pwdlib |
| Data Models | Pydantic |
| Token Handling | python‑jose |
| Runtime | Python 3.13 |

---

## 📁 **Project Structure**

```
mini_social_feed/
│
├── main.py
│
├── requirements.txt
├── README.md
│
├── databases/
│   └── database.py
│
├── models/
│   ├── user_models.py
│   └── auth_models.py
│
├── routers/
│   ├── auth_routers.py
│   ├── users_routers.py
│   ├── posts_routers.py
│   ├── likes_routers.py
│   ├── comments_routers.py
│   └── feed_routers.py
│
├── schemas/
│   ├── users_schemas.py
│   ├── auth_schema.py
│   ├── posts_schemas.py
│   └── feed_schemas.py
│
├── services/
│   ├── users_services.py
│   ├── auth_services.py
│   └── config.py
│
└── To-do List
```

---

## 🔐 **Environment Variables Setup**

This project uses environment variables for security‑sensitive configuration.

### **1. Rename `.env_example` → `.env`**

Inside the project root:

```
mv .env_example .env
```

### **2. Open `.env` and add your values**

Example:

```
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
UPLOAD_DIR=uploads
```

### **3. Load environment variables in `config.py`**

The project uses `python-dotenv` to load `.env`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
```

This ensures your secrets are not hard‑coded and remain secure.

---

## 📄 **What Each File Does**

### **main.py**
Initializes FastAPI, loads routers, and starts the application.

### **config.py**
Loads environment variables and exposes configuration values such as:

- JWT secret  
- Algorithm  
- Token expiration  
- Upload directory  

### **schema.py**
Defines all Pydantic models:

- `UserCreate` — registration input  
- `UserPublic` — safe response model  
- `UserInDB` — internal model with hashed password  
- `LoginRequest` — login payload  

### **routers/auth.py**
Handles all authentication logic:

- `/register`
- `/login`
- `/logout`
- `/refresh`
- `/me`

Includes:

- Password hashing  
- Token creation  
- Token verification  
- Current user dependency  
- In‑memory user storage  

### **routers/posts.py** *(future)*  
# Mini Social Feed API

A backend API for a social media app where users can create posts (with optional images), like posts, comment, follow users, and view a personalized feed.

## Features
- User registration, login, logout, and token refresh
- User profiles (bio, avatar, display name)
- Follow/unfollow users
- Create, update, delete posts (with optional images)
- Like/unlike posts (idempotent)
- Comment on posts, delete comments
- Personalized feed (posts from followed users and self)
- Pagination and search support

## Roles
- User (default)
- Admin (optional moderation)

## API Endpoints

### Auth
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login
- `POST /auth/refresh` — Refresh token
- `POST /auth/logout` — Logout
- `GET /auth/me` — Get current user info

### Users
- `GET /users/{username}` — Public profile
- `PATCH /users/me` — Update profile
- `POST /users/{username}/follow` — Follow user
- `DELETE /users/{username}/follow` — Unfollow user
- `GET /users/{username}/followers` — List followers
- `GET /users/{username}/following` — List following

### Posts
- `POST /posts/` — Create post (auth required)
- `GET /posts/` — List posts (public feed, supports pagination, search, sort)
- `GET /posts/{post_id}` — View single post
- `PATCH /posts/{post_id}` — Update post (owner only)
- `DELETE /posts/{post_id}` — Delete post (owner/admin)

### Likes
- `POST /likes/posts/{post_id}/like` — Like post (auth required)
- `DELETE /likes/posts/{post_id}/like` — Unlike post (auth required)
- `GET /likes/posts/{post_id}/likes` — List users who liked

### Comments
- `POST /comments/posts/{post_id}/comments` — Add comment (auth required)
- `GET /comments/posts/{post_id}/comments` — List comments (paginated)
- `DELETE /comments/{comment_id}` — Delete comment (owner/admin)

### Feed
- `GET /feed/` — Personalized feed (auth required, paginated)

## Database Models
- **users**: id, username, email, password_hash, bio, avatar_url, role, timestamps
- **posts**: id, user_id, title, content, image_url, visibility, timestamps
- **likes**: id, post_id, user_id, unique(post_id, user_id), timestamps
- **comments**: id, post_id, user_id, content, timestamps
- **follows**: follower_id, following_id, unique(follower_id, following_id)
- **refresh_tokens**: id, user_id, token_hash, revoked_at, expires_at

## Setup
1. Clone the repo
2. Install dependencies (`pip install -r requirements.txt`)
3. Run the app (`uvicorn main:app --reload`)

## Notes
- Endpoints are stubbed; business logic and database integration required.
- Designed for FastAPI.


---

## ⚙️ **Setup Instructions**

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/mini_social_feed.git
cd mini_social_feed
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables  
Rename `.env_example` → `.env` and add your secret key.

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. Open API docs

Visit:

```
http://127.0.0.1:8000/docs
```

---

## 🔑 **Authentication Flow**

1. **Register** → `/auth/register`  
2. **Login** → `/auth/login`  
   - Returns access + refresh tokens  
3. **Authorize** using the access token  
4. **Access protected routes**  
5. **Refresh token** → `/auth/refresh`  
6. **Logout** → `/auth/logout`  

---

## 📬 **API Endpoints Summary As at Now**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Login and receive tokens |
| GET | `/auth/me` | Get current authenticated user |
| POST | `/auth/logout` | Revoke refresh token |
| POST | `/auth/refresh` | Generate new access token |

