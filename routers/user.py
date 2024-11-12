
from fastapi import APIRouter
from .. import schemas, database, models
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
from .. hashing import Hash
from ..oauth2 import get_current_user
from .. import oauth2
from fastapi import  File, UploadFile, Response, status
import shutil
import os

get_db = database.get_db
router = APIRouter()






@router.post('/user', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserCreation)
def create_user(request: schemas.UserCreation, db: Session=Depends(get_db)):
    new_user = models.User(
        username = request.username,
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email,
        bio = request.bio,
        password = Hash.bcrypt(request.password)
        
    )
    db.add(new_user) 
    db.commit()
    db.refresh(new_user) 
    return request 

@router.get('/user',response_model=List[schemas.showUser])
def Users(db: Session=Depends(get_db)):
    user_list = db.query(models.User).all() 
    return user_list 


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def User_Detail(id: UUID, db: Session=Depends(get_db)):
    profile = db.query(models.User).filter(models.User.id == id).first()
    return profile

@router.put('/user/{id}')
async def update_user(
    id: UUID,
    request: schemas.UserCreation,
    response: Response,
    db: Session = Depends(get_db),
    profile_photo: UploadFile = File(None),
    cover_photo: UploadFile = File(None)
):
    update_data = request.model_dump()

    # Handle password hashing if needed
    if 'password' in update_data and update_data['password']:
        update_data['password'] = Hash.bcrypt(update_data['password'])

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': 'User not found'}

    # Handle profile photo upload 
    if profile_photo:
        profile_photo_path = f"media/profile_photos/{id}_{profile_photo.filename}"
        with open(profile_photo_path, "wb") as buffer:
            shutil.copyfileobj(profile_photo.file, buffer)
        update_data['profile_photo'] = profile_photo_path

    # Handle cover photo upload
    if cover_photo:
        cover_photo_path = f"media/cover_photos/{id}_{cover_photo.filename}"
        with open(cover_photo_path, "wb") as buffer:
            shutil.copyfileobj(cover_photo.file, buffer)
        update_data['cover_photo'] = cover_photo_path

    # Update user data
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {'detail': 'User has been updated', 'user': user}

@router.delete('/user/{id}', status_code=202)
def delete_user(id, response: Response,  db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    if not user:
        response.status_code =status.HTTP_404_NOT_FOUND
        return {'detail': 'User not found in the system'}
    db.commit()
    return {'detail': 'User has been deletd'}  