from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

acervo_livros = {
    1: {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "status": "disponível"},
    2: {"titulo": "1984", "autor": "George Orwell", "status": "disponivel"},
}

usuarios_cadastrados = {
    "michael": "senha123",
    "joao": "qweasd"
}

class Aluguel(BaseModel):
    nome: str
    senha: str
    id_livro: int

@app.post("/alugar")
def alugar_livro(dados: Aluguel):
    
    if dados.nome not in usuarios_cadastrados:
        raise(HTTPException(status_code=401, detail="Usuário não encontrado"))
    
    if dados.senha != usuarios_cadastrados[dados.nome]:
        raise HTTPException(status_code=401, detail="senha incorreta")
    
    if dados.id_livro not in acervo_livros:
        raise HTTPException(status_code=401, detail={"erro" : "Livro não encontrado"})
    
    livro = acervo_livros[dados.id_livro]

    if livro["status"] == "alugado":
        raise HTTPException(status_code=401, detail={"erro" : "Livro já alugado"})
    
    livro["status"] = "alugado"
 
    return {"Sucesso" : f"O livro {livro["titulo"]} foi alugado!"}
