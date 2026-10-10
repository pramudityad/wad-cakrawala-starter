# backend/ — Pelatihan HR (demo Sesi 9–10)

FastAPI + SQLAlchemy + Alembic. Login memakai JWT di cookie `httpOnly`.

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                              # isi JWT_SECRET; .env tidak di-commit
export $(grep -v '^#' .env | xargs)               # muat env ke shell
alembic upgrade head                              # terapkan migrasi
ADMIN_PASSWORD=ganti-ini python seed.py           # 6 sesi + admin@example.com
uvicorn app.main:app --reload
pytest -q                                         # 9 tes: 401/403/409, N+1, cookie
```

Lihat SQL yang dijalankan: `SQL_ECHO=1 uvicorn app.main:app`.
Database lain: ubah `DATABASE_URL` (mis. `postgresql+psycopg://…`, tambah `pip install psycopg[binary]`).

## Peta demo

| Persyaratan lab | Di mana |
|---|---|
| Model one-to-many | `app/orm.py` |
| Migrasi dibaca + applied | `alembic/versions/` (2 migrasi) |
| Session per request, `finally` | `app/db.py` `get_db` |
| UNIQUE di database → 409 | `Registration`, `main.py` `register` |
| Tanpa N+1 | `selectinload` di `list_sessions`, dites `test_list_has_no_n_plus_one` |
| Hash bcrypt, JWT cookie, RBAC, otorisasi objek | `app/auth.py`, `get_own_registration` |
