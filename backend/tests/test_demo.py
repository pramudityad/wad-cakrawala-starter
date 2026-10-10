import os
from datetime import date

os.environ["JWT_SECRET"] = "test-secret-test-secret-test-secret-123"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import hash_password
from app.db import Base, get_db
from app.main import app
from app.orm import TrainingSession, User

PW = "kata-sandi-panjang"


@pytest.fixture
def env():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Local = sessionmaker(bind=engine, autoflush=False)

    def override():
        db = Local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override
    with Local() as db:
        db.add(User(email="admin@t.io", password_hash=hash_password(PW), role="admin"))
        db.add_all(TrainingSession(judul=f"s{i}", tanggal=date(2026, 10, 1), pemateri="x", kapasitas=5) for i in range(5))
        db.commit()
    yield engine
    app.dependency_overrides.clear()


def client_for(email, register=True):
    c = TestClient(app)
    if register:
        assert c.post("/auth/register", json={"email": email, "password": PW}).status_code == 201
    assert c.post("/auth/login", json={"email": email, "password": PW}).status_code == 200
    return c


def test_no_token_is_401(env):
    assert TestClient(app).get("/sessions").status_code == 401


def test_user_token_on_admin_route_is_403(env):
    assert client_for("a@t.io").delete("/sessions/1").status_code == 403


def test_admin_can_delete(env):
    assert client_for("admin@t.io", register=False).delete("/sessions/1").status_code == 204


def test_other_users_registration_is_403(env):
    a, b = client_for("a@t.io"), client_for("b@t.io")
    reg = a.post("/sessions/1/registrations").json()
    assert a.get(f"/registrations/{reg['id']}").status_code == 200
    assert b.get(f"/registrations/{reg['id']}").status_code == 403  # ganti id di URL
    assert b.delete(f"/registrations/{reg['id']}").status_code == 403


def test_duplicate_registration_is_409_from_database(env):
    a = client_for("a@t.io")
    assert a.post("/sessions/1/registrations").status_code == 201
    assert a.post("/sessions/1/registrations").status_code == 409


def test_duplicate_email_is_409(env):
    client_for("a@t.io")
    assert TestClient(app).post("/auth/register", json={"email": "a@t.io", "password": PW}).status_code == 409


def test_no_password_or_hash_in_responses(env):
    c = TestClient(app)
    r = c.post("/auth/register", json={"email": "a@t.io", "password": PW})
    assert "password" not in r.text and "hash" not in r.text
    me = client_for("b@t.io").get("/auth/me")
    assert set(me.json()) == {"id", "email", "role"}


def test_cookie_is_httponly_lax(env):
    c = TestClient(app)
    c.post("/auth/register", json={"email": "a@t.io", "password": PW})
    h = c.post("/auth/login", json={"email": "a@t.io", "password": PW}).headers["set-cookie"].lower()
    assert "httponly" in h and "samesite=lax" in h


def test_list_has_no_n_plus_one(env):
    a = client_for("a@t.io")
    for i in range(1, 6):
        a.post(f"/sessions/{i}/registrations")
    sql = []
    event.listen(env, "before_cursor_execute", lambda *args: sql.append(args[2]))
    assert len(a.get("/sessions").json()) == 5
    assert len(sql) == 3  # user + sesi + registrasi — tetap 3 berapa pun jumlah sesi
