import os

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from app.data import SESSIONS, next_id
from app.model import SessionIn, SessionOut

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


@app.get("/sessions")
def list_sessions(skip: int = 0, limit: int = 10, search: str | None = None) -> list[SessionOut]:
    data = SESSIONS
    if search:
        needle = search.lower()
        data = [s for s in data if needle in s["judul"].lower() or needle in s["pemateri"].lower()]
    return data[skip : skip + limit]


@app.get("/sessions/{session_id}")
def get_session(session_id: int) -> SessionOut:
    for s in SESSIONS:
        if s["id"] == session_id:
            return s
    raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")


@app.post("/sessions", status_code=201)
def create_session(payload: SessionIn) -> SessionOut:
    session = {"id": next_id(), **payload.model_dump()}
    SESSIONS.append(session)
    return session


@app.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int):
    for i, s in enumerate(SESSIONS):
        if s["id"] == session_id:
            SESSIONS.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Sesi tidak ditemukan")
