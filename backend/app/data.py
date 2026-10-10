from datetime import date

SESSIONS: list[dict] = [
    {"id": 1, "judul": "onboarding karyawan baru", "tanggal": date(2026, 10, 1), "pemateri": "Sari", "kapasitas": 20, "terdaftar": 15},
    {"id": 2, "judul": "keselamatan kerja", "tanggal": date(2026, 10, 2), "pemateri": "Sari", "kapasitas": 20, "terdaftar": 15},
    {"id": 3, "judul": "dasar-dasar payroll", "tanggal": date(2026, 10, 3), "pemateri": "Budi", "kapasitas": 15, "terdaftar": 15},
    {"id": 4, "judul": "komunikasi efektif", "tanggal": date(2026, 10, 6), "pemateri": "Rina", "kapasitas": 25, "terdaftar": 10},
    {"id": 5, "judul": "manajemen waktu", "tanggal": date(2026, 10, 7), "pemateri": "Rina", "kapasitas": 25, "terdaftar": 22},
    {"id": 6, "judul": "etika kerja", "tanggal": date(2026, 10, 8), "pemateri": "Budi", "kapasitas": 20, "terdaftar": 5},
    {"id": 7, "judul": "keselamatan kebakaran", "tanggal": date(2026, 10, 9), "pemateri": "Joko", "kapasitas": 30, "terdaftar": 30},
    {"id": 8, "judul": "pelatihan p3k", "tanggal": date(2026, 10, 10), "pemateri": "Joko", "kapasitas": 20, "terdaftar": 18},
    {"id": 9, "judul": "onboarding tim IT", "tanggal": date(2026, 10, 13), "pemateri": "Sari", "kapasitas": 12, "terdaftar": 12},
    {"id": 10, "judul": "kepemimpinan dasar", "tanggal": date(2026, 10, 14), "pemateri": "Dewi", "kapasitas": 18, "terdaftar": 9},
    {"id": 11, "judul": "layanan pelanggan", "tanggal": date(2026, 10, 15), "pemateri": "Dewi", "kapasitas": 20, "terdaftar": 20},
    {"id": 12, "judul": "penggunaan sistem absensi", "tanggal": date(2026, 10, 16), "pemateri": "Budi", "kapasitas": 25, "terdaftar": 3},
]


def next_id() -> int:
    return max((s["id"] for s in SESSIONS), default=0) + 1
