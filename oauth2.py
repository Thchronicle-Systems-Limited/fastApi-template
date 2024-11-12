from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, Response, HTTPException
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from . import models
import token
from .  token import verify_token
from sqlalchemy.orm import Session
from . import models
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    user = db.query(models.User).filter(models.User.username == token_data.username).first()

    if not user:
        raise credentials_exception

    return user