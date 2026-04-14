from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# --- BANCO DE DADOS TEMPORÁRIO ---

# Ajuste 1: Usamos as Tags RFID como chaves (Strings) em vez de números inteiros,
# pois é isso que o seu leitor ACR122U envia para o app.
acervo_livros = {
    "A1B2C3D4": {"titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "status": "disponível"},
    "F272FB03": {"titulo": "1984", "autor": "George Orwell", "status": "disponível"},
    "C3BF872D": {"titulo": "Clean Code", "autor": "Robert C. Martin", "status": "disponível"}
}

# Ajuste 2: Mudamos para 'cpf' para bater com o campo que o seu ModalAutenticacao envia.
usuarios_cadastrados = {
    "12345678900": "1234",
    "123": "321"
}

# Dicionário para rastrear: { "TAG_RFID": "CPF_DO_USUARIO" }
livros_alugados = {}


# --- MODELOS DE DADOS (Pydantic) ---

# Ajuste 3: O modelo deve refletir exatamente o JSON que o seu fetch() envia.
# No seu React, você envia: { cpf, senha, livros: [id1, id2...] }
class PedidoAluguel(BaseModel):
    cpf: str
    senha: str
    livros: List[str]  # Uma lista de Strings (os RFIDs bipados)


class ConsultaRFID(BaseModel):
    rfid: str


# --- ROTAS (ENDPOINTS) ---

# Ajuste 4: Rota de Consulta (Necessária para a TelaAluguel e TelaAPI)
# O seu app faz um POST para consultar cada livro assim que você bipa.
@app.post("/api/livros/consultar")
def consultar_livro(dados: ConsultaRFID):
    if dados.rfid not in acervo_livros:
        # Erro 404 para o app exibir o Alert de "Livro não cadastrado"
        raise HTTPException(status_code=404, detail="Livro não encontrado no acervo")

    livro = acervo_livros[dados.rfid]
    alugado = dados.rfid in livros_alugados

    return {
        "rfid": dados.rfid,
        "nomeLivro": livro["titulo"],
        "disponivel": not alugado,
        "mensagem": "Indisponível" if alugado else "Disponível"
    }


# Ajuste 5: Rota de Teste (GET) para o botão "Testar Conexão" da TelaAPI
@app.get("/api/livros/consultar")
def ping_servidor():
    return {"status": "online", "mensagem": "FastAPI rodando perfeitamente"}


# Ajuste 6: Rota de Aluguel Final
@app.post("/api/aluguel/confirmar")
def confirmar_aluguel(dados: PedidoAluguel):
    # Validação de Usuário (CPF)
    if dados.cpf not in usuarios_cadastrados:
        raise HTTPException(status_code=401, detail="Usuário não cadastrado")

    # Validação de Senha
    if dados.senha != usuarios_cadastrados[dados.cpf]:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    # Verificação de disponibilidade de todos os livros da lista
    for rfid in dados.livros:
        if rfid in livros_alugados:
            nome = acervo_livros.get(rfid, {}).get("titulo", rfid)
            raise HTTPException(status_code=400, detail=f"O livro '{nome}' já está alugado")
        if rfid not in acervo_livros:
            raise HTTPException(status_code=400, detail=f"Tag {rfid} não pertence ao acervo")

    # Se todos passarem, processamos o aluguel
    for rfid in dados.livros:
        livros_alugados[rfid] = dados.cpf
        acervo_livros[rfid]["status"] = "alugado"
        print(f"📖 Livro {rfid} alugado para {dados.cpf}")

    return {"status": "sucesso", "mensagem": f"{len(dados.livros)} livro(s) alugado(s) com sucesso!"}


# --- INICIALIZAÇÃO ---

if __name__ == '__main__':
    # Ajuste 7: Importante rodar no host 0.0.0.0 para o celular conseguir conectar via Wi-Fi.
    # A porta 5000 é a que você já configurou no app.
    uvicorn.run(app, host="0.0.0.0", port=5000)