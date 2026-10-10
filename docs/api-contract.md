# Kontrak API

API pelatihan HR: admin membuat sesi pelatihan, karyawan mendaftar dan membatalkan pendaftaran.
Base URL lokal: `http://localhost:8000`. Base URL produksi: diisi di Sesi 14.

## Model data

| Tabel | Kolom |
|---|---|
| `users` | id, email (unik), password_hash (tidak pernah dikembalikan), role (`user`/`admin`) |
| `sessions` | id, judul, tanggal, pemateri, kapasitas |
| `registrations` | id, session_id (FK), user_id (FK), unik (session_id, user_id) |

Satu sesi punya banyak registrasi (one-to-many); satu pengguna tidak bisa mendaftar dua kali ke sesi yang sama.

## Autentikasi

`POST /auth/login` menaruh JWT (berlaku 1 jam) di cookie `access_token` — `httpOnly`, `SameSite=Lax`,
`Secure` di produksi. Klien memakai `credentials: "include"`; token tidak pernah terlihat oleh JavaScript.

## Endpoint

| Endpoint | Auth | Balasan |
|---|---|---|
| `POST /auth/register` `{email, password≥8}` | publik | 201 `{id,email,role}`; 409 email sudah ada |
| `POST /auth/login` | publik | 200 + cookie; 401 `Email atau password salah` |
| `POST /auth/logout` | publik | 204, cookie dihapus |
| `GET /auth/me` | login | 200 `{id,email,role}` |
| `GET /sessions?skip&limit&search` | login | 200 daftar sesi + `registrations` + `terdaftar` |
| `GET /sessions/{id}` | login | 200; 404 |
| `POST /sessions` `{judul,tanggal,pemateri,kapasitas}` | admin | 201; 422 isian salah |
| `DELETE /sessions/{id}` | admin | 204; 404 |
| `POST /sessions/{id}/registrations` | login | 201 milik pemanggil; 409 sudah terdaftar |
| `GET` / `DELETE /registrations/{id}` | pemilik atau admin | 200 / 204; 403 bukan milikmu |

Contoh error: `{"detail": "Bukan registrasi milikmu"}`.

## Status code yang dipakai

| Kode | Kapan |
|---|---|
| 200 / 201 / 204 | berhasil / dibuat / berhasil tanpa badan |
| 401 | tidak login atau token tidak valid — kami tidak tahu siapa kamu |
| 403 | login, tapi bukan admin atau bukan pemilik objek |
| 404 | id tidak ada |
| 409 | pelanggaran UNIQUE di database (email atau pendaftaran ganda) |
| 422 | bentuk isian salah (divalidasi Pydantic sebelum menyentuh database) |

## Versioning

Perubahan yang memecahkan kontrak ini diumumkan di thread kelompok sebelum digabung ke `main`.
