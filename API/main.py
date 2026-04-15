# main.py
from fastapi import FastAPI
import uvicorn
from routers import livros, aluguel

app = FastAPI(title="Biblioteca API")

# Aqui nós "plugamos" os mini-aplicativos no aplicativo principal
app.include_router(livros.router)
app.include_router(aluguel.router)

if __name__ == '__main__':
    # Dica: Passar "main:app" como string permite usar o reload=True via código
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)