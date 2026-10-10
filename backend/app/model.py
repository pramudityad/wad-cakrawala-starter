from datetime import date

from pydantic import BaseModel, ConfigDict, computed_field


class SessionIn(BaseModel):
    judul: str
    tanggal: date
    pemateri: str
    kapasitas: int


class RegistrationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    user_id: int


class SessionOut(SessionIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registrations: list[RegistrationOut] = []

    @computed_field
    @property
    def terdaftar(self) -> int:
        return len(self.registrations)
