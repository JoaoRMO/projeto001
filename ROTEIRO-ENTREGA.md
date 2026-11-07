# Roteiro de organização e entrega – Prática Avaliada 1 (Semana 4)

Projeto: **Dighanger.com** · Ferramenta: **Visual Studio** (ou VS Code para o Python)
Tema dos exemplos: cadastro e uso de **looks** (7 looks: camiseta, calça/bermuda, tênis, nº de usos, data do último uso).

## 1. Estrutura final de pastas

```
projeto001/
├── ROTEIRO-ENTREGA.md          (este guia – não precisa entregar)
├── NOTA-USO-IA.md              (nota exigida no enunciado – ENTREGAR)
├── exercicio-1/arquitetura-backend.html
├── exercicio-2/analise-http.txt
├── exercicio-3/api-ecommerce.md
└── exercicio-4/
    ├── main.py                 (arquivo pedido)
    ├── requirements.txt
    ├── test_main.py            (testes, opcional)
    └── main_looks.py           (BÔNUS com o tema looks, opcional)
```
Os nomes dos arquivos seguem exatamente o enunciado. Não renomeie.

## 2. Exercício 1 – `arquitetura-backend.html` (2 pts)

**Abrir/ajustar no Visual Studio**
1. *Arquivo → Abrir → Pasta* e escolha `projeto001`.
2. Abra `exercicio-1/arquitetura-backend.html`. Para ver no navegador: botão direito → *Exibir no navegador* (ou dê duplo clique no arquivo).
3. Confira no navegador os 4 critérios:
   - [ ] Fluxo completo (cliente → backend → banco e volta) – seção 2
   - [ ] Papel do backend – seção 1 (+ HTTP na 3, hardware × software na 4, APIs na 5)
   - [ ] HTML semântico: `header`, `nav`, `main`, `section`, `figure`, `footer` (use *Ctrl+F* para conferir)
   - [ ] Diagrama em CSS (caixas coloridas e setas) – redimensione a janela para ver a versão móvel.
4. **Personalize**: troque o texto do `<footer>` pelo seu nome/turma e, se quiser, a URL `api.dighanger.com` pela real.

## 3. Exercício 2 – `analise-http.txt` (2 pts)

1. Abra o arquivo e leia cada parte (A, B, C).
2. Confira:
   - [ ] **Parte A**: request line, 3 cabeçalhos, linha em branco e corpo explicados
   - [ ] **Parte B**: 201, 404, 401, 400 (ou 422), 500
   - [ ] **Parte C**: GET, POST, PUT, DELETE, cada um com exemplo (usando os looks)
3. **Ajustes**: acrescente com suas palavras uma frase sobre por que escolheu 400 ou 422 (o FastAPI usa 422). Salve como **UTF-8** (Visual Studio: *Arquivo → Salvar como → seta ao lado de Salvar → Salvar com codificação → UTF-8*), para os acentos não quebrarem.

## 4. Exercício 3 – `api-ecommerce.md` (3 pts)

1. Abra o `.md` (no Visual Studio: *Ctrl+Shift+V* no VS Code mostra a prévia; no Visual Studio instale a extensão *Markdown Editor* se quiser a prévia).
2. **Atenção ao enunciado**: ele pede "e-commerce com produtos e pedidos". Adaptei para **Looks** (no lugar de produtos) e **Usos** (no lugar de pedidos), com tabela de equivalência na seção 0. Se o professor exigir os nomes originais, faça *Localizar e Substituir* (Ctrl+H): `looks → produtos`, `usos → pedidos` (revise o texto depois). Se quiser, pergunte antes ao professor/tutor se o tema pode ser adaptado.
3. Confira:
   - [ ] Endpoints REST (seção 1)
   - [ ] 2 exemplos completos de requisição/resposta (seção 2)
   - [ ] HATEOAS com `_links` (seção 3)
   - [ ] Erros padronizados (seção 4)

## 5. Exercício 4 – `main.py` (3 pts)

**Preparar o ambiente (uma vez)** – abra o terminal do Visual Studio (*Exibir → Terminal*) na pasta `exercicio-4`:
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (no Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```
**Rodar**
```bash
uvicorn main:app --reload
```
Abra http://127.0.0.1:8000/docs (Swagger) e teste:
1. `POST /usuarios` com `{"nome": "Maria Silva", "email": "maria@exemplo.com"}` → **201**
2. `GET /usuarios` → lista com a Maria
3. Repita o POST → **409** (e-mail duplicado)
4. POST com `"email": "abc"` → **422** (validação Pydantic)

**Testes automáticos (opcional)**
```bash
python test_main.py
```
Confira os critérios:
- [ ] Estrutura FastAPI (`app = FastAPI(...)`, decoradores)
- [ ] 2 endpoints: `POST /usuarios` e `GET /usuarios`
- [ ] Pydantic: `UsuarioCreate`/`Usuario` com `EmailStr`, `Field`
- [ ] Tratamento de erros: `HTTPException` 409 e 400
- [ ] Armazenamento em memória (lista `usuarios`)

> `main_looks.py` é um **bônus** com o seu tema (7 looks e registro de usos). Rode com `uvicorn main_looks:app --reload`. O enunciado pede usuários, então o **`main.py` é o que vale** para a nota; entregue o bônus só se quiser mostrar o projeto.

## 6. Antes de entregar

1. **Leia e entenda** cada arquivo. Ajuste frases com suas palavras, o enunciado recomenda entender o código, não só copiar.
2. **Preencha `NOTA-USO-IA.md`** com o link da conversa (obrigatório quando se usa IA).
3. Verifique os nomes: `arquitetura-backend.html`, `analise-http.txt`, `api-ecommerce.md`, `main.py`.
4. Não envie `.venv/` nem `__pycache__/` (o `.gitignore` já ignora).
5. **Como entregar**: pelo repositório GitHub (envie o link da branch/repositório) ou compactando as 4 pastas em `.zip`, conforme a plataforma da disciplina pedir.

## 7. Git no Visual Studio (se a entrega for pelo GitHub)
*Git → Confirmar ou Estashar* (mensagem, ex.: "Prática avaliada 1") → *Enviar* (push). Pelo terminal:
```bash
git add .
git commit -m "Prática Avaliada 1 - Semana 4"
git push
```
