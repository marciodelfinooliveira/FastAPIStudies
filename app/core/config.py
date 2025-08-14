import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Configurações da aplicação, carregadas a partir de variáveis de ambiente.
    """
    
    # --- Configurações da Aplicação FastAPI ---
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(60, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    
    # --- Configuração do Banco de Dados PostgreSQL ---
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # --- Configuração do Redis ---
    REDIS_URL: str = Field("redis://redis:6379/0", env="REDIS_URL")
    
    # --- Configuração do Kafka ---
    KAFKA_BROKERS: str = Field("kafka:9092", env="REDPANDA_KAFKA_BROKERS")
    
    # --- Configuração do Servidor SMTP (MailHog) ---
    SMTP_HOST: str = Field("mailhog", env="SMTP_HOST")
    SMTP_PORT: int = Field(1025, env="SMTP_PORT")

    class Config:
        # Define o arquivo .env a ser lido
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()