from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Esquema para a resposta do token de acesso.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Esquema para os dados contidos dentro do token JWT.
    """
    email: Optional[str] = None
