"""Isi data awal: python seed.py (setelah alembic upgrade head)."""
import os
import secrets
from datetime import date

from sqlalchemy import select

from app.db import SessionLocal
from app.auth import hash_password
from app.orm import TrainingSession, User

SESSIONS = [
    ("onboarding karyawan baru", date(2026, 10, 1), "Sari", 20),
    ("keselamatan kerja", date(2026, 10, 2), "Sari", 20),
    ("dasar-dasar payroll", date(2026, 10, 3), "Budi", 15),
    ("komunikasi efektif", date(2026, 10, 6), "Rina", 25),
    ("manajemen waktu", date(2026, 10, 7), "Rina", 25),
    ("etika kerja", date(2026, 10, 8), "Budi", 20),
]

with SessionLocal() as db:
    if db.scalar(select(TrainingSession.id).limit(1)) is None:
        db.add_all(TrainingSession(judul=j, tanggal=t, pemateri=p, kapasitas=k) for j, t, p, k in SESSIONS)
        db.commit()
    if db.scalar(select(User.id).where(User.role == "admin")) is None:
        password = os.getenv("ADMIN_PASSWORD") or secrets.token_urlsafe(12)
        db.add(User(email="admin@example.com", password_hash=hash_password(password), role="admin"))
        db.commit()
        print(f"admin@example.com / {password}  (simpan; tidak ditampilkan lagi)")
    print("seed ok")
