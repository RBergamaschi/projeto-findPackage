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
from datetime import datetime, timezone, timedelta

from app.configs.environment import get_environment_settings
from app.core.exceptions import UnauthorizedException


env = get_environment_settings()

SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = env.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = env.REFRESH_TOKEN_EXPIRE_DAYS

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")