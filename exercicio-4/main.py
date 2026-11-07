"""
Prática Avaliada 1 - Exercício 4
API REST com FastAPI - Gerenciamento de usuários (Dighanger.com)

Os usuários são as pessoas donas dos guarda-roupas/looks do Dighanger.com.

Executar:
    uvicorn main:app --reload
Documentação interativa (Swagger):
    http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="Dighanger.com - API de Usuários",
    description="Cadastro e listagem de usuários (armazenamento em memória).",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Modelos Pydantic (validação de dados)
# ---------------------------------------------------------------------------
class UsuarioCreate(BaseModel):
    """Dados que o cliente envia para criar um usuário (sem id)."""
    nome: str = Field(..., min_length=2, max_length=100, examples=["Maria Silva"])
    email: EmailStr = Field(..., examples=["maria@exemplo.com"])


class Usuario(UsuarioCreate):
    """Usuário completo: id gerado pelo servidor + nome + email."""
    id: int


# ---------------------------------------------------------------------------
# "Banco de dados" em memória
# ---------------------------------------------------------------------------
usuarios: list[Usuario] = []
proximo_id: int = 1


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate) -> Usuario:
    """Cria um usuário. Retorna 201; 409 se o e-mail já estiver cadastrado."""
    global proximo_id

    email = dados.email.lower()
    if any(u.email.lower() == email for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um usuário cadastrado com o e-mail {dados.email}.",
        )

    nome = dados.nome.strip()
    if len(nome) < 2:  # espaços não contam como nome
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome não pode ser vazio.",
        )

    usuario = Usuario(id=proximo_id, nome=nome, email=dados.email)
    usuarios.append(usuario)
    proximo_id += 1
    return usuario


@app.get("/usuarios", response_model=list[Usuario])
def listar_usuarios() -> list[Usuario]:
    """Lista todos os usuários cadastrados."""
    return usuarios
