from datetime import date

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user", server_default="user")


class TrainingSession(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    judul: Mapped[str] = mapped_column(String(200))
    tanggal: Mapped[date]
    pemateri: Mapped[str] = mapped_column(String(100))
    kapasitas: Mapped[int]
    registrations: Mapped[list["Registration"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class Registration(Base):
    __tablename__ = "registrations"
    # Constraint di database: Pydantic bukan lapisan terakhir
    __table_args__ = (UniqueConstraint("session_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    session: Mapped[TrainingSession] = relationship(back_populates="registrations")
