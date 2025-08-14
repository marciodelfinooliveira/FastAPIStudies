from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

class UserService:
    """
    Serviço para encapsular a lógica de negócio relacionada aos usuários.
    """

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Busca um usuário pelo seu endereço de e-mail.

        Args:
            db: A sessão assíncrona do banco de dados.
            email: O e-mail do usuário a ser buscado.

        Returns:
            O objeto User se encontrado, caso contrário None.
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """
        Cria um novo usuário no banco de dados.

        Args:
            db: A sessão assíncrona do banco de dados.
            user_in: Os dados do usuário a ser criado, validados pelo esquema Pydantic.

        Returns:
            O objeto User recém-criado.
        """
        
        hashed_password = get_password_hash(user_in.password)
        
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            password=hashed_password
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user

    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário, verificando e-mail e senha.

        Args:
            db: A sessão assíncrona do banco de dados.
            email: O e-mail do usuário.
            password: A senha em texto plano a ser verificada.

        Returns:
            O objeto User se a autenticação for bem-sucedida, caso contrário None.
        """
        user = await self.get_user_by_email(db, email=email)
        
        if not user or not verify_password(password, user.password):
            return None
            
        return user

user_service = UserService()
