# SICAT Backend

## Guia Docker (recomendado)

1. **Instale o Docker**  
   Baixe e instale em: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

2. **Suba banco, backend e phpMyAdmin:**
```bash
cd backend
docker compose up --build
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

