import datetime

import jose
import passlib.context

import core.settings

pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = core.settings.settings


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(
    data: dict,
) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jose.jwt.encode(
        to_encode, core.settings.settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> bool:
    try:
        payload = jose.jwt.decode(
            token, core.settings.settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jose.JWTError:
        return None
