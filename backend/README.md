# SICAT Backend

## Instalação

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
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

