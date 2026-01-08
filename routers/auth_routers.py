# authentication logic
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from schemas.auth_schema import UserCreate, UserPublic, UserInDB, LoginRequest, TokenRefreshRequest, PasswordResetRequest, PasswordResetConfirm
from services.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from databases.database import users_db, refresh_tokens_db
import uuid


router = APIRouter()

# password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_hash = PasswordHash.recommended()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# HELPER FUNCTIONS
def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=401, detail="Invalid claims (check issuer or audience)")
    except jwt.JWTError as e:
        # This catches signature mismatches or malformed strings
        print(f"JWT Decode Error: {str(e)}")
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")


def create_email_verification_token(user_id: str):
    return jwt.encode(
        {
            "sub": user_id,
            "type": "email_verify",
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_password_reset_token(user_id: str):
    return jwt.encode(
        {
            "sub": user_id,
            "type": "password_reset",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# --- Dependency ---
def get_current_user_dep(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    # Check if refresh token is revoked
    token_entry = refresh_tokens_db.get(user_id)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    if token_entry and token_entry.get("revoked") is True:
        raise HTTPException(
            status_code=401, detail="Token has been revoked. Please log in again.")
    # check if user exists in dictionary database
    for user in users_db.values():
        if str(user.id) == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


def get_current_active_user_dep(current_user: UserInDB = Depends(get_current_user_dep)):
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ----------------------- #
# ENDPOINTS


@router.post("/register", response_model=UserPublic, status_code=201)
def register(user_data: UserCreate):
    if user_data.username in users_db:
        raise HTTPException(
            status_code=409, detail="Username already registered")

    for u in users_db.values():
        if u.email == user_data.email:
            raise HTTPException(status_code=409, detail="Email already exists")

    user_id = str(uuid.uuid4())
    hashed_pw = hash_password(user_data.password)

    new_user = UserInDB(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        role="user",
        is_email_verified=False,
        email_verified_at=None,
        created_at=datetime.now(timezone.utc)
    )

    users_db[user_data.username] = new_user
    email_token = create_email_verification_token(user_id)
    print(
        f"Verify email link: "
        f"http://localhost:8000/auth/verify-email?token={email_token}"
    )
    return UserPublic(**new_user.dict())


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    # Find user by username or email
    user = None
    for u in users_db.values():
        if u.username == request.username or u.email == request.username:
            user = u
            break
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_email_verified:
        raise HTTPException(
            status_code=403, detail="Please verify your email first")

    user_id = str(user.id)
    # Create tokens
    access_token = create_access_token(
        data={"sub": user_id, "role": user.role}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(
        data={"sub": user_id}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    # store refresh token
    refresh_tokens_db[user_id] = {
        "refresh_token": refresh_token, "revoked": False}
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserPublic)
def read_current_user(current_user: dict = Depends(get_current_user_dep)):
    return current_user


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user_id = payload.get("sub")
    if user_id in refresh_tokens_db:
        refresh_tokens_db[user_id]["revoked"] = True
        print(refresh_tokens_db[user_id])
        del refresh_tokens_db[user_id]
    return {"msg": "Logged out successfully done."}


@router.post("/refresh")
def refresh_access_token(request: TokenRefreshRequest):
    # Verify  the incoming refresh token
    payload = verify_token(request.refresh_token)
    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = str(payload.get("sub"))
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid or revoked refresh token")
    # Check if token belong to user
    token_entry = refresh_tokens_db.get(user_id)
    # 3. Content Match - Let's see exactly what's failing
    stored_token = token_entry["refresh_token"]
    provided_token = request.refresh_token

    if stored_token != provided_token:
        raise HTTPException(status_code=401, detail="Token mismatch")
    if token_entry.get("revoked") is True:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    # 4. Content Match
    if token_entry["refresh_token"] != request.refresh_token:
        raise HTTPException(status_code=401, detail="Token mismatch")
    # Find the user to get their current role
    user = None
    for u in users_db.values():
        if str(u.id) == user_id:
            user = u
            break
    if not user:
        raise HTTPException(
            status_code=404, detail="User associated with this token no longer exists")
    # issue new access token
    new_access_token = create_access_token(
        data={"sub": user_id, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user_id},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    # Overwrite old refresh token (rotation)
    refresh_tokens_db[user_id] = {
        "refresh_token": new_refresh_token,
        "revoked": False,
    }
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/verify-email")
def verify_email(token: str):
    payload = verify_token(token)

    if payload.get("type") != "email_verify":
        raise HTTPException(
            status_code=400, detail="Invalid verification token")

    user_id = payload.get("sub")

    for user in users_db.values():
        if str(user.id) == user_id:
            user.is_email_verified = True
            user.email_verified_at = datetime.now(timezone.utc)
            return {"message": "Email verified successfully"}

    raise HTTPException(status_code=404, detail="User not found")


@router.post("/password-reset/request")
def request_password_reset(data: PasswordResetRequest):
    user = None
    for u in users_db.values():
        if u.email == data.email:
            user = u
            break

    if not user:
        return {"message": "If email exists, a reset link has been sent"}

    reset_token = create_password_reset_token(str(user.id))

    print(
        f"Reset password link: http://localhost:8000/auth/password-reset/confirm?token={reset_token}")

    return {"message": "If email exists, a reset link has been sent"}


@router.post("/password-reset/confirm")
def confirm_password_reset(data: PasswordResetConfirm):
    payload = verify_token(data.token)

    if payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid token type")

    user_id = payload.get("sub")

    for user in users_db.values():
        if str(user.id) == user_id:
            user.hashed_password = hash_password(data.new_password)
            return {"message": "Password reset successful"}

    raise HTTPException(status_code=404, detail="User not found")
