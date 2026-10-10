import os
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.orm import User

# Tanpa JWT_SECRET: secret acak per proses (token mati saat restart) — tidak pernah di-hardcode.
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)
JWT_ALGORITHM = "HS256"
TOKEN_TTL = timedelta(hours=1)
COOKIE_NAME = "access_token"
COOKIE_SECURE = os.getenv("COOKIE_SECURE") == "1"  # 1 di produksi (https)

router = APIRouter(prefix="/auth", tags=["auth"])


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)  # 72 = batas byte bcrypt


class UserOut(BaseModel):
    id: int
    email: str
    role: str

    model_config = {"from_attributes": True}


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Autentikasi: siapa kamu? Gagal -> 401."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Belum login")
    try:
        user_id = int(jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token tidak valid")
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Token tidak valid")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """Otorisasi (RBAC): boleh melakukan apa? Gagal -> 403."""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin")
    return user


@router.post("/register", status_code=201)
def register(creds: Credentials, db: Session = Depends(get_db)) -> UserOut:
    user = User(email=creds.email.lower(), password_hash=hash_password(creds.password))  # role selalu "user"
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email sudah terdaftar")
    return user


@router.post("/login")
def login(creds: Credentials, response: Response, db: Session = Depends(get_db)) -> UserOut:
    user = db.scalar(select(User).where(User.email == creds.email.lower()))
    # Pesan sama untuk email salah dan password salah: jangan bocorkan akun mana yang ada.
    if user is None or not verify_password(creds.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.now(timezone.utc) + TOKEN_TTL},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        max_age=int(TOKEN_TTL.total_seconds()),
    )
    return user


@router.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME, httponly=True, secure=COOKIE_SECURE, samesite="lax")


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> UserOut:
    return user
