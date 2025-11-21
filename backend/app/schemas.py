from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import TipoUsuario, StatusFicha

class UsuarioBase(BaseModel):
    cpf: str
    matricula: str
    nome_completo: str

class UsuarioCreate(UsuarioBase):
    senha: str
    confirmar_senha: str

class RegistroRequest(BaseModel):
    matricula: str
    senha_suap: str
    nova_senha: str
    confirmar_senha: str

class UsuarioResponse(UsuarioBase):
    id: str
    tipo: TipoUsuario
    data_registro: datetime
    data_edicao: datetime
    biblioteca: Optional[dict] = None  
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    matricula: str
    senha: str

class LoginResponse(BaseModel):
    token: str
    tipo: TipoUsuario

class RecuperarAcessoRequest(BaseModel):
    matricula: str
    senha_suap: str
    nova_senha: str
    confirmar_senha: str

class FichaCatalograficaBase(BaseModel):
    autor_nome_completo: str
    autor_sobrenome: str
    autor_nome_sem_ultimo_sobrenome: str
    autor_ultimo_sobrenome: str
    orientador_nome_completo: Optional[str] = None
    orientador_sobrenome: Optional[str] = None
    orientador_nome_sem_ultimo_sobrenome: Optional[str] = None
    orientador_ultimo_sobrenome: Optional[str] = None
    coorientador_nome_completo: Optional[str] = None
    coorientador_sobrenome: Optional[str] = None
    coorientador_nome_sem_ultimo_sobrenome: Optional[str] = None
    coorientador_ultimo_sobrenome: Optional[str] = None
    titulo: str
    subtitulo: Optional[str] = None
    data_dia: str
    data_mes: str
    data_ano: str
    cidade: str
    campus: str
    programa: str
    nivel_ensino: str
    curso: str
    palavras_chave: str
    tipo_trabalho: str

class FichaCatalograficaCreate(FichaCatalograficaBase):
    biblioteca_id: str

class FichaCatalograficaResponse(FichaCatalograficaBase):
    id: str
    id_curto: str
    status: StatusFicha
    data_criacao: datetime
    imagem_png: Optional[str] = None 
    pdf_tcc: Optional[str] = None
    biblioteca_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class AprovarNegarRequest(BaseModel):
    aprovado: bool

class ModificarTipoRequest(BaseModel):
    tipo: TipoUsuario

class BibliotecaBase(BaseModel):
    nome: str
    campus: str

class BibliotecaCreate(BibliotecaBase):
    pass

class BibliotecaResponse(BibliotecaBase):
    id: str
    data_criacao: datetime
    data_edicao: datetime
    
    class Config:
        from_attributes = True

class AdicionarBibliotecarioRequest(BaseModel):
    usuario_id: str
    biblioteca_id: str

class BibliotecarioBibliotecaResponse(BaseModel):
    id: str
    usuario_id: str
    biblioteca_id: str
    data_criacao: datetime
    
    class Config:
        from_attributes = True
