from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_current_user
from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.services.user_service import user_service
from app.core.security import create_access_token, create_refresh_token
from app.db.models.user import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user_endpoint(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db_session)
):
    """
    Endpoint para criar um novo usuário.
    """
    existing_user = await user_service.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um usuário com este e-mail já está cadastrado.",
        )
    
    user = await user_service.create_user(db, user_in=user_in)
    return user

@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint para autenticar o usuário e retornar tokens de acesso e refresh.
    """
    user = await user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Dados a serem incluídos no payload do token
    token_data = {"sub": user.email}
    
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint protegido que retorna os dados do usuário logado.
    """
    return current_user
