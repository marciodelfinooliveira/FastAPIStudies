from typing import AsyncGenerator, Optional
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.schemas.token import TokenData
from app.db.models.user import User
from app.services.user_service import user_service

# 'tokenUrl' aponta para o endpoint de login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependência que fornece uma sessão de banco de dados por requisição.
    Garante que a sessão seja sempre fechada após o uso.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    db: AsyncSession = Depends(get_db_session), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependência para obter o usuário atual a partir de um token JWT.
    Protege os endpoints que a utilizam.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Valida o payload com o esquema Pydantic
        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    # Busca o usuário no banco de dados
    user = await user_service.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
        
    return user
