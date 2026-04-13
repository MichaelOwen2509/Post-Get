from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

acervo_livros = {
    1: {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "status": "disponível"},
    2: {"titulo": "1984", "autor": "George Orwell", "status": "alugado"},
}

usuarios_cadastrados = {
    "michael": "senha123",
    "joao": "qweasd"
}

class RequisicaoAluguel(BaseModel):
    nome_usuario: str
    senha: str
    livro_id: int

@app.post("/alugar/")
def alugar_livro(dados: RequisicaoAluguel):
    
    if dados.nome_usuario not in usuarios_cadastrados:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
        
    if usuarios_cadastrados[dados.nome_usuario] != dados.senha:
        raise HTTPException(status_code=401, detail="Senha incorreta.")
        
    if dados.livro_id not in acervo_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
        
    livro = acervo_livros[dados.livro_id]
    
    if livro["status"] == "alugado":
        raise HTTPException(status_code=400, detail="Este livro já está alugado por outra pessoa.")
        
    livro["status"] = "alugado"
    
    return {
        "mensagem": f"Parabéns {dados.nome_usuario}, aluguel aprovado!",
        "livro_alugado": livro["titulo"]
    }