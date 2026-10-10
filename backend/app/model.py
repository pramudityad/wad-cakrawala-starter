from datetime import date

from pydantic import BaseModel


class SessionIn(BaseModel):
    judul: str
    tanggal: date
    pemateri: str
    kapasitas: int
    terdaftar: int = 0


class SessionOut(SessionIn):
    id: int
