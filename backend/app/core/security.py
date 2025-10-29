from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


class TokenData(BaseModel):
    email: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            return None

        return TokenData(email=email)
    except JWTError:
        return None

