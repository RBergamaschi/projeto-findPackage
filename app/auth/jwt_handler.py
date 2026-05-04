'''
Por que usar o PyJWT para autenticação?
O PyJWT é uma biblioteca Python que facilita a criação e verificação de JSON Web Tokens (JWTs). 
Ele é amplamente utilizado para autenticação e autorização em aplicações web. 
Aqui estão algumas razões pelas quais o PyJWT é uma escolha popular para autenticação:

1. Simplicidade: O PyJWT é fácil de usar e tem uma API simples para criar e verificar tokens JWT.
2. Segurança: O PyJWT suporta algoritmos de assinatura seguros, como HS256 e RS256, para garantir a integridade dos tokens.
3. Flexibilidade: O PyJWT permite que você inclua informações personalizadas no payload do token, o que pode ser útil para armazenar dados do usuário ou permissões.
4. Compatibilidade: O PyJWT é compatível com a maioria dos frameworks web Python, como Flask e Django, facilitando a integração em suas aplicações.
5. Comunidade ativa: O PyJWT tem uma comunidade ativa de desenvolvedores, o que significa que você pode encontrar suporte e recursos facilmente.
'''


import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth.security import verify_password
from app.configs.database import get_db_connection
from app.configs.environment import get_environment_settings
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User
from app.schemas.user_schema import UserRead


env = get_environment_settings()
security = HTTPBearer()


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            env.SECRET_KEY,
            algorithms=[env.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")


async def authenticate_user(
    email: str,
    password: str,
    db: AsyncSession
) -> Optional[User]:
    result = await db.execute(
        select(User)
        .where(User.email == email)
    )
    
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db_connection)
) -> User:
    payload = verify_token(credentials.credentials)
    user_id_str = payload.get("sub")
    
    if not user_id_str:
        raise UnauthorizedException("Invalid token")
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedException("Invalid token")
    
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.address))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise UnauthorizedException("User not found")

    return user

def verify_address_ownership(
    address_owner_id: int, 
    user: User
) -> None:
    if address_owner_id != user.id:
        raise ForbiddenException("You do not have permission to access this resource")