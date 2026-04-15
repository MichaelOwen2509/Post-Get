# routers/aluguel.py
from fastapi import APIRouter, HTTPException
from schemas import PedidoAluguel
from database import acervo_livros, usuarios_cadastrados, livros_alugados

router = APIRouter(prefix="/aluguel", tags=["Aluguel"])

@router.post("/confirmar")
def confirmar_aluguel(dados: PedidoAluguel):
    if dados.cpf not in usuarios_cadastrados:
        raise HTTPException(status_code=401, detail="Usuário não cadastrado")

    if dados.senha != usuarios_cadastrados[dados.cpf]:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    for rfid in dados.livros:
        if rfid in livros_alugados:
            nome = acervo_livros.get(rfid, {}).get("titulo", rfid)
            raise HTTPException(status_code=400, detail=f"O livro '{nome}' já está alugado")
        if rfid not in acervo_livros:
            raise HTTPException(status_code=400, detail=f"Tag {rfid} não pertence ao acervo")

    for rfid in dados.livros:
        livros_alugados[rfid] = dados.cpf
        acervo_livros[rfid]["status"] = "alugado"
        print(f"Livro {rfid} alugado para {dados.cpf}")

    return {"status": "sucesso", "mensagem": f"{len(dados.livros)} livro(s) alugado(s) com sucesso!"}