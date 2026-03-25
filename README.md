# SICAT Backend

## Docker (API + MySQL no host)

Use o MySQL que já roda na VPS, com **outro database** (ex.: `sicat`).

1. Criar o banco (uma vez):

```sql
CREATE DATABASE sicat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configurar o projeto:

```bash
cp env.example .env
nano .env
```

- **`DATABASE_URL`**: `mysql+pymysql://USUARIO:SENHA@host.docker.internal:3306/sicat` (ajuste usuário, senha; caracteres especiais na senha → URL encode).
- **`SECRET_KEY`**: defina uma chave forte para este projeto.

3. Subir:

```bash
docker compose up --build -d
```

API na porta **7000**; documentação em **`/docs`**.

Se o container **não conectar** ao MySQL (ex.: MySQL só em `127.0.0.1`), ou ajuste o MySQL para aceitar conexões da interface do host / `bind-address`, ou rode o backend **sem Docker** (secção abaixo) com `127.0.0.1` no `DATABASE_URL`.

---

## Instalação sem Docker

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

`.env` com `DATABASE_URL` usando `127.0.0.1:3306` e banco `sicat`.

```bash
uvicorn main:app --host 0.0.0.0 --port 7000
```

---

## VPS Ubuntu (resumo)

1. [Instalar Docker Engine + Compose](https://docs.docker.com/engine/install/ubuntu/).
2. Clonar o repositório, criar `.env`, `docker compose up --build -d`.
3. Firewall: liberar **22** e **7000** (ou **80/443** se usar proxy reverso).

Logs e atualização:

```bash
docker compose logs -f backend
git pull && docker compose up --build -d
```
