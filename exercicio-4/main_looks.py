"""
BÔNUS (não faz parte do enunciado) - mesma ideia do main.py, aplicada ao
tema do Dighanger.com: cadastro de looks e registro de usos.

Executar:  uvicorn main_looks:app --reload   ->  http://127.0.0.1:8000/docs
"""
from datetime import date

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Dighanger.com - Looks (bônus)", version="1.0.0")


class LookCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=60)
    camiseta: str = Field(..., min_length=3, description="Cor da camiseta")
    bottom_tipo: str = Field(..., pattern="^(calça|bermuda)$")
    bottom_cor: str = Field(..., min_length=3)
    tenis: str = Field(..., min_length=3, description="Cor do tênis")


class Look(LookCreate):
    id: int
    vezes_usado: int = 0
    ultimo_uso: date | None = None


class UsoCreate(BaseModel):
    data: date


class Uso(UsoCreate):
    id: int
    look_id: int
    total_acumulado: int


def _look(id, nome, camiseta, tipo, cor, tenis, vezes, ultimo):
    return Look(id=id, nome=nome, camiseta=camiseta, bottom_tipo=tipo,
                bottom_cor=cor, tenis=tenis, vezes_usado=vezes, ultimo_uso=ultimo)


looks: list[Look] = [
    _look(1, "Casual Clássico", "branca", "calça", "jeans azul", "branco", 18, date(2026, 11, 5)),
    _look(2, "Esportivo", "preta", "bermuda", "cinza", "preto", 11, date(2026, 11, 3)),
    _look(3, "Fim de Semana", "branca", "bermuda", "jeans", "preto", 12, date(2026, 11, 1)),
    _look(4, "Trabalho Descontraído", "cinza", "calça", "preta", "preto", 9, date(2026, 10, 30)),
    _look(5, "Noturno", "preta", "calça", "jeans preta", "cinza", 12, date(2026, 11, 2)),
    _look(6, "Verão Colorido", "amarela", "bermuda", "bege", "branco", 5, date(2026, 10, 20)),
    _look(7, "Street", "verde", "calça", "cargo", "vermelho", 3, date(2026, 10, 10)),
]
usos: list[Uso] = []


def _buscar(look_id: int) -> Look:
    for look in looks:
        if look.id == look_id:
            return look
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Look {look_id} não encontrado.")


@app.get("/looks", response_model=list[Look])
def listar_looks():
    return looks


@app.get("/looks/{look_id}", response_model=Look)
def obter_look(look_id: int):
    return _buscar(look_id)


@app.post("/looks", response_model=Look, status_code=status.HTTP_201_CREATED)
def criar_look(dados: LookCreate):
    novo = Look(id=max((l.id for l in looks), default=0) + 1, **dados.model_dump())
    looks.append(novo)
    return novo


@app.post("/looks/{look_id}/usos", response_model=Uso, status_code=status.HTTP_201_CREATED)
def registrar_uso(look_id: int, dados: UsoCreate):
    look = _buscar(look_id)
    if dados.data > date.today():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "A data não pode estar no futuro.")
    look.vezes_usado += 1
    if look.ultimo_uso is None or dados.data > look.ultimo_uso:
        look.ultimo_uso = dados.data
    uso = Uso(id=len(usos) + 1, look_id=look_id, data=dados.data, total_acumulado=look.vezes_usado)
    usos.append(uso)
    return uso


@app.get("/looks/{look_id}/usos", response_model=list[Uso])
def historico_usos(look_id: int):
    _buscar(look_id)
    return [u for u in usos if u.look_id == look_id]
