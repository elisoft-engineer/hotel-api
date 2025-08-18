from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError, JWTClaimsError, ExpiredSignatureError
from passlib.context import CryptContext

from core.conf import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    

def create_token(token_type: TokenType, data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME) \
            if token_type == TokenType.ACCESS else timedelta(days=settings.REFRESH_TOKEN_LIFETIME)
    to_encode.update({"exp": expire, "type": "access" if token_type == TokenType.ACCESS else "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except (JWTClaimsError, JWTError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def verify_token(token: str, token_type: TokenType) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get('type') != token_type.value:
            raise HTTPException(status_code=401, detail=f"Invalid {token_type} token")
        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except (JWTClaimsError, JWTError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
