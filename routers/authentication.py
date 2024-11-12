from fastapi import APIRouter
from .. import schemas, database, models, token
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
from .. hashing import Hash
from ..schemas import Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm

get_db = database.get_db
router = APIRouter()


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
        
    access_token = token.create_access_token(
        data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
