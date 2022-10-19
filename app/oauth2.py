from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import models
from .schemas import login_schema
from .database import get_db
from .creds import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    data_to_encode = data.copy()
    expires_on = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expires_on})

    access_token = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
    return access_token


def get_token_data(token: str, credential_exception) -> login_schema.TokenData:
    """Validates the token and returns its payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = login_schema.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to authorize",
        headers={"WWW-Authenticate": "Bearer"})

    token_data = get_token_data(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
