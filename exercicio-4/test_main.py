"""Testes rápidos: pytest  (ou rode: python test_main.py)"""
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_listar_vazio():
    main.usuarios.clear(); main.proximo_id = 1
    r = client.get("/usuarios")
    assert r.status_code == 200 and r.json() == []


def test_criar_e_listar():
    main.usuarios.clear(); main.proximo_id = 1
    r = client.post("/usuarios", json={"nome": "Maria Silva", "email": "maria@exemplo.com"})
    assert r.status_code == 201
    assert r.json() == {"nome": "Maria Silva", "email": "maria@exemplo.com", "id": 1}
    assert len(client.get("/usuarios").json()) == 1


def test_email_invalido():
    assert client.post("/usuarios", json={"nome": "Ana", "email": "invalido"}).status_code == 422


def test_campo_faltando():
    assert client.post("/usuarios", json={"nome": "Ana"}).status_code == 422


def test_email_duplicado():
    main.usuarios.clear(); main.proximo_id = 1
    client.post("/usuarios", json={"nome": "Maria", "email": "m@x.com"})
    assert client.post("/usuarios", json={"nome": "Outra", "email": "M@x.com"}).status_code == 409


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_"):
            fn(); print("OK ", nome)
