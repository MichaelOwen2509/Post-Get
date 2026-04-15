# routers/livros.py
from fastapi import APIRouter, HTTPException
from schemas import ConsultaRFID
from database import acervo_livros, livros_alugados

router = APIRouter(prefix="/livros", tags=["Livros"])

@router.post("/consultar")
def consultar_livro(dados: ConsultaRFID):
    if dados.rfid not in acervo_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado no acervo")

    livro = acervo_livros[dados.rfid]
    alugado = dados.rfid in livros_alugados

    return {
        "rfid": dados.rfid,
        "nomeLivro": livro["titulo"],
        "disponivel": not alugado,
        "mensagem": "Indisponível" if alugado else "Disponível"
    }

@router.get("/consultar")
def ping_servidor():
    return {"status": "online", "mensagem": "FastAPI rodando perfeitamente"}