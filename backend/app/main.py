import os

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.model import RegistrationIn, RegistrationOut, SessionIn, SessionOut
from app.orm import Registration, TrainingSession

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


def get_session_or_404(db: Session, session_id: int) -> TrainingSession:
    obj = db.get(TrainingSession, session_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")
    return obj


@app.get("/sessions")
def list_sessions(
    skip: int = 0, limit: int = 10, search: str | None = None, db: Session = Depends(get_db)
) -> list[SessionOut]:
    # selectinload: 2 query total (sesi + registrasi), bukan 1 + N
    stmt = select(TrainingSession).options(selectinload(TrainingSession.registrations))
    if search:
        like = f"%{search}%"  # nilai dikirim sebagai parameter, bukan disusun ke SQL
        stmt = stmt.where(TrainingSession.judul.ilike(like) | TrainingSession.pemateri.ilike(like))
    return db.scalars(stmt.order_by(TrainingSession.id).offset(skip).limit(limit)).all()


@app.get("/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)) -> SessionOut:
    return get_session_or_404(db, session_id)


@app.post("/sessions", status_code=201)
def create_session(payload: SessionIn, db: Session = Depends(get_db)) -> SessionOut:
    obj = TrainingSession(**payload.model_dump())
    db.add(obj)
    db.commit()
    return obj


@app.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_db)):
    db.delete(get_session_or_404(db, session_id))
    db.commit()
    return Response(status_code=204)


@app.post("/sessions/{session_id}/registrations", status_code=201)
def register(
    session_id: int, payload: RegistrationIn, db: Session = Depends(get_db)
) -> RegistrationOut:
    get_session_or_404(db, session_id)
    reg = Registration(session_id=session_id, user_id=payload.user_id)
    db.add(reg)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Sudah terdaftar di sesi ini")
    return reg
