from imports import *
from typing import ClassVar

class Client(BaseModel):
    id: int = 0
    nombre: str = ""
    correo: str = ""
    rfc: str = ""
    fecha_alta: datetime
    format_date: ClassVar[str] = "%d/%m/%Y"

    @validator("fecha_alta", pre=True)
    def get_date(cls,value):
        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, cls.format_date)
        except ValueError:
            raise ValueError(f"Client::get_date: Error, el formato no es valido: fecha: {value} formato requerido: {cls.format_date}")