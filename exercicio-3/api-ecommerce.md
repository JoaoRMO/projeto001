# API RESTful – Dighanger.com (Cadastro e Uso de Looks)

**Prática Avaliada 1 – Exercício 3**

## 0. Contexto e adaptação do tema

O enunciado pede uma API REST para um "e-commerce simples" com **Produtos** e **Pedidos**. A estrutura abaixo mantém exatamente os mesmos conceitos de design (coleção + registros que se relacionam por chave estrangeira, status, total, estoque/contadores), aplicados ao projeto **Dighanger.com**:

| Entidade do enunciado | Entidade no Dighanger.com | Observação |
|---|---|---|
| Produto (`id, nome, preco, categoria, estoque`) | **Look** (`id, nome, camiseta, bottom_tipo, bottom_cor, tenis, vezes_usado`) | `categoria` → `ocasiao`, `estoque` → `vezes_usado` (contador) |
| Pedido (`id, produto_id, quantidade, total, status`) | **Uso** (`id, look_id, data, quantidade, total_acumulado, status`) | Cada registro de uso de um look em uma data |

> Obs.: se o professor exigir os nomes originais, basta trocar nos exemplos: `looks → produtos` e `usos → pedidos`. A modelagem é idêntica.

### Dados de exemplo (7 looks)

| id | nome | ocasião | camiseta | bottom | tênis | vezes_usado | último uso |
|---|---|---|---|---|---|---|---|
| 1 | Casual Clássico | casual | branca | calça jeans azul | branco | 18 | 2026-11-05 |
| 2 | Esportivo | esporte | preta | bermuda cinza | preto | 11 | 2026-11-03 |
| 3 | Fim de Semana | casual | branca | bermuda jeans | preto | 12 | 2026-11-01 |
| 4 | Trabalho Descontraído | trabalho | cinza | calça preta | preto | 9 | 2026-10-30 |
| 5 | Noturno | noite | preta | calça jeans preta | cinza | 12 | 2026-11-02 |
| 6 | Verão Colorido | verão | amarela | bermuda bege | branco | 5 | 2026-10-20 |
| 7 | Street | urbano | verde | calça cargo | vermelho | 3 | 2026-10-10 |

---

## 1. Design dos endpoints REST

**Base URL:** `https://api.dighanger.com/v1`
**Formato:** JSON (`Content-Type: application/json`) · **Autenticação:** `Authorization: Bearer <token>`

Princípios aplicados: URLs com **substantivos no plural**, sem verbos; **método HTTP** define a ação; **status codes** corretos; recursos aninhados para relacionamentos; **versionamento** na URL.

### Looks

| Método | Endpoint | Descrição | Sucesso | Erros |
|---|---|---|---|---|
| GET | `/looks` | Lista looks (filtros: `?ocasiao=casual`, `?camiseta=preta`, paginação `?page=1&limit=10`) | 200 | 401 |
| GET | `/looks/{id}` | Detalha um look | 200 | 401, 404 |
| POST | `/looks` | Cadastra um look | 201 | 400, 401, 422 |
| PUT | `/looks/{id}` | Substitui todos os dados do look | 200 | 400, 401, 404, 422 |
| PATCH | `/looks/{id}` | Altera parcialmente (ex.: só o tênis) | 200 | 400, 401, 404, 422 |
| DELETE | `/looks/{id}` | Remove o look | 204 | 401, 404, 409 |

### Usos

| Método | Endpoint | Descrição | Sucesso | Erros |
|---|---|---|---|---|
| GET | `/usos` | Lista todos os usos (filtros: `?look_id=5`, `?de=2026-11-01&ate=2026-11-07`) | 200 | 401 |
| GET | `/usos/{id}` | Detalha um uso | 200 | 401, 404 |
| POST | `/looks/{id}/usos` | Registra o uso de um look (incrementa `vezes_usado`) | 201 | 400, 401, 404, 422 |
| GET | `/looks/{id}/usos` | Histórico de usos de um look | 200 | 401, 404 |
| PATCH | `/usos/{id}` | Altera status (ex.: `cancelado`) | 200 | 401, 404, 422 |
| DELETE | `/usos/{id}` | Remove um registro de uso (decrementa o contador) | 204 | 401, 404 |

### Modelo de dados

**Look**
```json
{
  "id": 5,
  "nome": "Noturno",
  "ocasiao": "noite",
  "camiseta": "preta",
  "bottom_tipo": "calça",
  "bottom_cor": "jeans preta",
  "tenis": "cinza",
  "vezes_usado": 12,
  "ultimo_uso": "2026-11-02"
}
```

**Uso**
```json
{
  "id": 41,
  "look_id": 5,
  "data": "2026-11-07",
  "quantidade": 1,
  "total_acumulado": 13,
  "status": "registrado"
}
```
`status` ∈ `registrado | cancelado`. `total_acumulado` é o valor de `vezes_usado` do look após o registro (análogo ao `total` do pedido).

---

## 2. Exemplos completos de requisição/resposta

### Exemplo 1 – Cadastrar um novo look (`POST /looks`)

**Requisição**
```http
POST /v1/looks HTTP/1.1
Host: api.dighanger.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

{
  "nome": "Look de Domingo",
  "ocasiao": "casual",
  "camiseta": "azul",
  "bottom_tipo": "bermuda",
  "bottom_cor": "bege",
  "tenis": "branco"
}
```

**Resposta – 201 Created**
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: https://api.dighanger.com/v1/looks/8
```
```json
{
  "id": 8,
  "nome": "Look de Domingo",
  "ocasiao": "casual",
  "camiseta": "azul",
  "bottom_tipo": "bermuda",
  "bottom_cor": "bege",
  "tenis": "branco",
  "vezes_usado": 0,
  "ultimo_uso": null,
  "_links": {
    "self":     { "href": "/v1/looks/8", "method": "GET" },
    "update":   { "href": "/v1/looks/8", "method": "PUT" },
    "delete":   { "href": "/v1/looks/8", "method": "DELETE" },
    "registrar_uso": { "href": "/v1/looks/8/usos", "method": "POST" },
    "usos":     { "href": "/v1/looks/8/usos", "method": "GET" },
    "colecao":  { "href": "/v1/looks", "method": "GET" }
  }
}
```

### Exemplo 2 – Registrar o uso de um look (`POST /looks/5/usos`)

**Requisição**
```http
POST /v1/looks/5/usos HTTP/1.1
Host: api.dighanger.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

{
  "data": "2026-11-07",
  "quantidade": 1
}
```

**Resposta – 201 Created**
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: https://api.dighanger.com/v1/usos/41
```
```json
{
  "id": 41,
  "look_id": 5,
  "data": "2026-11-07",
  "quantidade": 1,
  "total_acumulado": 13,
  "status": "registrado",
  "_links": {
    "self":    { "href": "/v1/usos/41", "method": "GET" },
    "look":    { "href": "/v1/looks/5", "method": "GET" },
    "cancelar":{ "href": "/v1/usos/41", "method": "PATCH" },
    "remover": { "href": "/v1/usos/41", "method": "DELETE" }
  }
}
```
Efeito colateral: o Look 5 passa a ter `vezes_usado = 13` e `ultimo_uso = 2026-11-07`.

---

## 3. HATEOAS (implementação básica)

**HATEOAS** (*Hypermedia As The Engine Of Application State*) faz a API **informar, em cada resposta, os links das ações possíveis**. O cliente não precisa "decorar" URLs: segue os links recebidos. Os links mudam conforme o **estado** do recurso.

### Convenção usada
Campo `_links` com objetos `{ "href": ..., "method": ... }` e nomes de relação (`self`, `update`, `delete`, `registrar_uso`...).

### Exemplo – `GET /v1/looks/5`
```json
{
  "id": 5,
  "nome": "Noturno",
  "camiseta": "preta",
  "bottom_tipo": "calça",
  "bottom_cor": "jeans preta",
  "tenis": "cinza",
  "vezes_usado": 12,
  "ultimo_uso": "2026-11-02",
  "_links": {
    "self":          { "href": "/v1/looks/5", "method": "GET" },
    "update":        { "href": "/v1/looks/5", "method": "PUT" },
    "delete":        { "href": "/v1/looks/5", "method": "DELETE" },
    "registrar_uso": { "href": "/v1/looks/5/usos", "method": "POST" },
    "usos":          { "href": "/v1/looks/5/usos", "method": "GET" },
    "colecao":       { "href": "/v1/looks", "method": "GET" }
  }
}
```

### Exemplo – coleção com paginação (`GET /v1/looks?page=1&limit=3`)
```json
{
  "items": [
    { "id": 1, "nome": "Casual Clássico", "vezes_usado": 18,
      "_links": { "self": { "href": "/v1/looks/1", "method": "GET" } } },
    { "id": 2, "nome": "Esportivo", "vezes_usado": 11,
      "_links": { "self": { "href": "/v1/looks/2", "method": "GET" } } },
    { "id": 3, "nome": "Fim de Semana", "vezes_usado": 12,
      "_links": { "self": { "href": "/v1/looks/3", "method": "GET" } } }
  ],
  "total": 7,
  "_links": {
    "self":  { "href": "/v1/looks?page=1&limit=3", "method": "GET" },
    "next":  { "href": "/v1/looks?page=2&limit=3", "method": "GET" },
    "criar": { "href": "/v1/looks", "method": "POST" }
  }
}
```

### Links dependentes de estado (Uso cancelado)
Um uso com `status: "cancelado"` **não** oferece o link `cancelar`:
```json
{
  "id": 40, "look_id": 2, "status": "cancelado",
  "_links": {
    "self":    { "href": "/v1/usos/40", "method": "GET" },
    "look":    { "href": "/v1/looks/2", "method": "GET" },
    "remover": { "href": "/v1/usos/40", "method": "DELETE" }
  }
}
```

---

## 4. Estrutura de tratamento de erros

### Formato padrão de erro
Todas as falhas retornam o mesmo envelope JSON (inspirado no RFC 7807), com o status HTTP correto:

```json
{
  "erro": {
    "codigo": "LOOK_NAO_ENCONTRADO",
    "mensagem": "Look com id 99 não foi encontrado.",
    "status": 404,
    "detalhes": [],
    "caminho": "/v1/looks/99",
    "timestamp": "2026-11-07T14:32:10Z"
  }
}
```

| Campo | Descrição |
|---|---|
| `codigo` | Identificador estável, legível por máquina (o cliente decide o que fazer a partir dele) |
| `mensagem` | Texto legível para humanos |
| `status` | Mesmo código do HTTP |
| `detalhes` | Lista com erros por campo (validação) |
| `caminho` / `timestamp` | Diagnóstico e rastreabilidade |

### Catálogo de erros

| Status | Código | Quando ocorre |
|---|---|---|
| 400 | `REQUISICAO_INVALIDA` | JSON malformado ou parâmetro inválido |
| 401 | `NAO_AUTENTICADO` | Token ausente, inválido ou expirado |
| 403 | `ACESSO_NEGADO` | Autenticado, mas tentando acessar look de outro usuário |
| 404 | `LOOK_NAO_ENCONTRADO` / `USO_NAO_ENCONTRADO` | Recurso inexistente |
| 405 | `METODO_NAO_PERMITIDO` | Ex.: `DELETE /looks` (na coleção) |
| 409 | `CONFLITO` | Ex.: excluir look que possui usos registrados, ou look duplicado |
| 422 | `ERRO_DE_VALIDACAO` | Campos faltando/inválidos (data futura, quantidade ≤ 0) |
| 429 | `MUITAS_REQUISICOES` | Limite de requisições excedido |
| 500 | `ERRO_INTERNO` | Falha inesperada (sem expor detalhes internos) |

### Exemplo – erro de validação (422)
`POST /v1/looks/5/usos` com `{"data": "2030-01-01", "quantidade": 0}`:
```json
{
  "erro": {
    "codigo": "ERRO_DE_VALIDACAO",
    "mensagem": "Os dados enviados são inválidos.",
    "status": 422,
    "detalhes": [
      { "campo": "data", "problema": "A data não pode estar no futuro." },
      { "campo": "quantidade", "problema": "Deve ser maior que zero." }
    ],
    "caminho": "/v1/looks/5/usos",
    "timestamp": "2026-11-07T14:35:02Z"
  }
}
```

### Exemplo – não autenticado (401)
```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer
```
```json
{
  "erro": {
    "codigo": "NAO_AUTENTICADO",
    "mensagem": "Token ausente ou expirado.",
    "status": 401,
    "detalhes": [],
    "caminho": "/v1/looks",
    "timestamp": "2026-11-07T14:40:00Z"
  }
}
```

### Boas práticas adotadas
- Nunca retornar *stack trace* ao cliente no `500` (apenas registrar em log no servidor).
- Mensagens claras, sem expor dados sensíveis.
- Erro sempre no mesmo formato, o que facilita o tratamento no frontend.
