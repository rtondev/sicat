# SICAT Backend

## Guia Docker (recomendado)

1. **Instale o Docker**  
   Baixe e instale em: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)  
   Em **Ubuntu VPS**, use o [guia oficial](https://docs.docker.com/engine/install/ubuntu/) (Docker Engine + plugin Compose).

2. **Suba banco, backend e phpMyAdmin:**
```bash
cd /caminho/do/sicat
cp env.example .env
# Ajuste SECRET_KEY e, se quiser, credenciais do MySQL em docker-compose.yml + DATABASE_URL
docker compose up --build -d
```

3. **Acessos:**
- **API** → [http://localhost:7000](http://localhost:7000)
- **Documentação (Swagger)** → [http://localhost:7000/docs](http://localhost:7000/docs)
- **phpMyAdmin** → [http://localhost:8080](http://localhost:8080) (servidor: `db`, usuário: `sicat_user`, senha: `sicat_password`)
- **MySQL** → `localhost:3306` (banco: `sicat`)

---

## Instalação (sem Docker)

1. Criar ambiente virtual:
```bash
python -m venv venv
```

2. Ativar ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar dependências:
```bash
pip install -r requirements.txt
```

## Executar

```bash
uvicorn main:app --reload --port 7000
```

O servidor estará disponível em `http://localhost:7000`

---

## Deploy em VPS Ubuntu (Docker)

1. **Instalar Docker e Compose** (resumo):
```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${VERSION_CODENAME:-$VERSION}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

2. **Colocar o projeto na VPS** (ex.: clonar o repositório na pasta desejada).

3. **Configurar `.env`** na raiz do projeto (mesmo diretório do `docker-compose.yml`):
```bash
cp env.example .env
nano .env
```
   - Com **Docker Compose**, use `DATABASE_URL` com host **`db`** e usuário/senha iguais aos definidos em `docker-compose.yml` (padrão do exemplo: `sicat_user` / `sicat_password`).
   - Defina um **`SECRET_KEY` forte** (não use o valor de exemplo em produção).

4. **Subir os serviços** (API na porta **7000**):
```bash
docker compose up --build -d
docker compose ps
curl -s http://127.0.0.1:7000/
```

5. **Firewall (UFW)** — se estiver ativo, libere a API (e opcionalmente só IP confiável):
```bash
sudo ufw allow 22/tcp
sudo ufw allow 7000/tcp
sudo ufw enable
sudo ufw status
```
   Em produção é mais seguro expor só **80/443** e usar **Nginx** (ou Traefik) como proxy reverso para `http://127.0.0.1:7000`, com TLS (Let’s Encrypt).

6. **phpMyAdmin** (opcional): o compose publica na porta **8080**; restrinja por firewall ou remova o serviço em produção se não for necessário.

7. **Logs e atualização**:
```bash
docker compose logs -f backend
docker compose pull   # se usar imagens públicas atualizadas
git pull && docker compose up --build -d
```

