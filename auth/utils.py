from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError, JWTClaimsError, ExpiredSignatureError

from core.conf import settings

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the Argon2id hasher with secure default parameters
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Hashes a plain text password using Argon2id."""
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plain text password against an Argon2id hash."""
    try:
        # argon2 expects (hash, password)
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False



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
