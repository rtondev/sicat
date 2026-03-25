from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.database import engine, Base
from app.routers import auth, fichas, admin, public, bibliotecarios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SICAT API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar diretório estático para servir arquivos
PUBLIC_DIR = Path(__file__).parent / "public"
PUBLIC_DIR.mkdir(exist_ok=True)
(PUBLIC_DIR / "pdfs").mkdir(exist_ok=True)
(PUBLIC_DIR / "imagens").mkdir(exist_ok=True)
app.mount("/public", StaticFiles(directory=str(PUBLIC_DIR)), name="public")

app.include_router(auth.router, prefix="/api/auth", tags=["autenticação"])
app.include_router(fichas.router, prefix="/api/fichas", tags=["fichas catalográficas"])
app.include_router(admin.router, prefix="/api/admin", tags=["administração"])
app.include_router(public.router, prefix="/api/public", tags=["público"])
app.include_router(bibliotecarios.router, prefix="/api/bibliotecarios", tags=["bibliotecários"])


@app.get("/")
def root():
    return {"message": "SICAT API"}

