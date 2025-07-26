from imports import *
from decimal import Decimal
from enum import Enum
from typing import ClassVar

class Status(Enum):
    activo = "activo"
    pagado = "pagado"
    vencido = "vencido"


class Loan(BaseModel):
    id: int = 0
    client_id: int = 0
    amount: float = 0.0000
    fecha_otorgamiento: datetime
    status: Status

    max_decimals: ClassVar[int] = 4
    format_date: ClassVar[str] = "%d/%m/%Y"


    @validator('amount')
    def max_two_decimals(cls, v):

        decimal_value = Decimal(str(v))
        
        if abs(decimal_value.as_tuple().exponent) > cls.max_decimals:
            raise ValueError(f'amount no puede tener más de {cls.max_decimals} decimales')
        
        return v
    
    @validator("fecha_otorgamiento", pre=True)
    def get_date(cls,value):

        if isinstance(value, datetime):
            return value

        try:
            return datetime.strptime(value, cls.format_date)
        except ValueError:
            raise ValueError(f"Client::get_date: Error, el formato no es valido: fecha: {value} formato requerido: {cls.format_date}")