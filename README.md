

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
├── config.py
├── schema.py
│
├── routers/
│   ├── auth.py
│   └── posts.py        (future expansion)
│
├── .env_example
├── requirements.txt
└── README.md
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
Placeholder for posts, likes, comments, feed, etc.

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

