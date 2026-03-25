# SICAT Backend

## Docker só da API (recomendado na VPS com MySQL já instalado)

Use o **mesmo servidor MySQL** de outros projetos (ex.: fluxomed), com **outro database** (ex.: `sicat`).

1. Crie o banco no MySQL do host (uma vez):

```sql
CREATE DATABASE sicat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Na pasta do projeto:

```bash
cp env.example .env
nano .env
```

- **`DATABASE_URL`**: usuário/senha iguais aos do MySQL do host; host **`host.docker.internal`** (traefik/docker resolve até o host); nome do banco **`sicat`**.
  - Exemplo com `root`:  
    `mysql+pymysql://root:SUA_SENHA@host.docker.internal:3306/sicat`  
  - Se a senha tiver `!`, `@`, etc., use encoding na URL (`!` → `%21`).
- **`SECRET_KEY`**: use uma chave **própria** do SICAT (não precisa ser a mesma do `JWT_SECRET` de outro app).

3. Suba só o backend:

```bash
docker compose up --build -d
```

A API fica em **porta 7000** (`/docs` para Swagger).

### Se der erro de conexão com o MySQL

Quando o MySQL só escuta em **`127.0.0.1`**, o container pode não alcançar via `host.docker.internal` dependendo da config. Nesse caso, no **Linux** use rede do host:

```bash
docker compose -f docker-compose.yml -f docker-compose.host-network.yml up --build -d
```

E no `.env`: `DATABASE_URL=...//usuario:senha@127.0.0.1:3306/sicat`.

**Outra opção** é no MySQL definir `bind-address = 0.0.0.0` e restringir acesso no firewall (menos comum se já está tudo na mesma VPS).

---

## Stack com MySQL dentro do Docker (opcional / dev)

Se **não** tiver MySQL no host:

```bash
docker compose -f docker-compose.bundled-mysql.yml up --build -d
```

Ajuste `.env` se não quiser usar o `DATABASE_URL` padrão definido nesse arquivo, ou confira as variáveis no próprio `docker-compose.bundled-mysql.yml`.

---

## Guia Docker (desktop / referência)

1. **Instale o Docker**  
   Desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)  
   **Ubuntu VPS**: [Docker Engine + Compose](https://docs.docker.com/engine/install/ubuntu/).

2. **Subir** (conforme cenário acima: só API, host-network, ou bundled MySQL).

3. **Acessos** (compose padrão só API):
   - **API** → `http://localhost:7000` (ou IP da VPS)
   - **Swagger** → `http://localhost:7000/docs`

---

## Instalação (sem Docker)

1. Criar ambiente virtual:

```bash
python -m venv venv
```

2. Ativar (Linux/Mac):

```bash
source venv/bin/activate
```

3. Instalar dependências:

```bash
pip install -r requirements.txt
```

4. `.env` com `DATABASE_URL` apontando para `127.0.0.1:3306` e banco `sicat`.

5. Executar:

```bash
uvicorn main:app --reload --port 7000
```

---

## Deploy em VPS Ubuntu (resumo)

1. Instalar Docker Engine + plugin Compose ([documentação](https://docs.docker.com/engine/install/ubuntu/)).
2. Clonar o repositório, criar `.env` (banco `sicat` no MySQL que já existe na VPS).
3. `docker compose up --build -d` (ou com `docker-compose.host-network.yml` se necessário).
4. UFW: liberar **22** e **7000** (ou só **80/443** se usar Nginx na frente).

Logs e atualização:

```bash
docker compose logs -f backend
git pull && docker compose up --build -d
```
