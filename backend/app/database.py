from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_hours: int = 72
    suap_api_url: str = "https://suap.ifrn.edu.br"
    
    class Config:
        env_file = ".env"

settings = Settings()

connect_args = {}
if 'pymysql' in settings.database_url:
    connect_args = {
        'connect_timeout': 120,
        'read_timeout': 600,
        'write_timeout': 600,
        'charset': 'utf8mb4'
    }

engine = create_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

