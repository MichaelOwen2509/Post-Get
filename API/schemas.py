# schemas.py
from pydantic import BaseModel
from typing import List

class PedidoAluguel(BaseModel):
    cpf: str
    senha: str
    livros: List[str] 

class ConsultaRFID(BaseModel):
    rfid: str