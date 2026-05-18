from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Nosso "banco de dados" em memória
livros = [
    {"id": 1, "titulo": "Engenharia de Software Moderna", "autor": "Valente"},
    {"id": 2, "titulo": "Clean Architecture", "autor": "Robert C. Martin"}
]


# Modelo de Dados (Pydantic) - Valida as entradas automaticamente
class Livro(BaseModel):
    id: Optional[int] = None
    titulo: str
    autor: str


@app.get("/")
def hello_world():
    return {"mensagem": "Hello, World! API FastAPI rodando."}


# GET: Listar todos os livros
@app.get("/api/livros")
def listar_livros():
    return {"livros": livros}


# POST: Adicionar um novo livro
@app.post("/api/livros", status_code=201)
def adicionar_livro(livro: Livro):
    # Converte o modelo validado para dicionário
    novo_livro = livro.dict(exclude_unset=True)
    novo_livro["id"] = len(livros) + 1
    livros.append(novo_livro)

    return {"mensagem": "Livro adicionado com sucesso!", "livro": novo_livro}


# GET: Buscar livro por ID
@app.get("/api/livros/{livro_id}")
def buscar_livro(livro_id: int):
    livro = next((l for l in livros if l["id"] == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


# PUT: Atualizar livro
@app.put("/api/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    livro = next((l for l in livros if l["id"] == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Atualiza apenas os campos enviados
    livro.update(livro_atualizado.dict(exclude_unset=True))
    return {"mensagem": "Livro atualizado com sucesso!", "livro": livro}


# DELETE: Remover livro
@app.delete("/api/livros/{livro_id}")
def deletar_livro(livro_id: int):
    livro = next((l for l in livros if l["id"] == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livros.remove(livro)
    return {"mensagem": "Livro removido com sucesso!"}

import uvicorn

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)