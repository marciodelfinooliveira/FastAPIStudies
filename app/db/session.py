from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cria a engine de banco de dados assíncrona
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # Logs Ativados para depuração 
    future=True
)

# Cria uma factory de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
