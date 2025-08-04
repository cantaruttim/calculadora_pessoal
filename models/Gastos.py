from pydantic import BaseModel

class Gastos(BaseModel):
    dono: str
    cartao: str
    vigencia: str
    valor: float
