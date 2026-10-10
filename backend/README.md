# backend/ — sengaja kosong

Kamu yang mengisi folder ini, mulai Sesi 2.

Sesi 2, yang harus ada di sini sebelum kamu keluar:

```
backend/
├── requirements.txt    # fastapi, uvicorn
└── app/
    ├── __init__.py
    └── main.py         # FastAPI() + GET /health -> 200 {"status": "ok"}
```

Titik mulai:

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install fastapi uvicorn
pip freeze > requirements.txt
uvicorn app.main:app --reload
```

`venv/` tidak di-commit — sudah diatur di `.gitignore`.

Hapus berkas ini kalau sudah tidak perlu.

<!-- applikasi internal yang digunakan oleh tim HR -->
<!-- untuk training session tracker // training komunikasi, training kesehatan -->

<!-- venv/ virtual environment -->
1. project HR tracker
- python. 
- fastapi v1.0


2. project absensi mahasiswa
- python
- fastapi v1.8


requirement
1. GET /sessions 
2. GET /sessions/{}
3. POST /sessions
4. DELETE /sessions/{}

pov admin
1. create, delete, get 
