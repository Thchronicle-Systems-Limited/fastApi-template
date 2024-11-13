
from fastapi import APIRouter
import schemas, database, models, oauth2
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
from oauth2 import get_current_user
import oauth2
from  hashing import Hash
from fastapi import  File, UploadFile, Response, status

get_db = database.get_db
router = APIRouter()

import shutil
import os
from fastapi import UploadFile

async def save_file(file: UploadFile, folder: str):
    # Ensure the media folder exists
    os.makedirs(f"media/{folder}", exist_ok=True)

    # Define the file location
    file_location = f"media/{folder}/{file.filename}"

    # Save the file to the specified location
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_location


@router.get('/users/me', response_model=schemas.User)
def myProfile(current_user: schemas.User = Depends(get_current_user)):
    return current_user

from fastapi import Form

@router.put('/user/me', status_code=status.HTTP_200_OK)
async def update_user(
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(None),
    bio: str = Form(...),
    current_user: models.User = Depends(get_current_user),
    profile_photo: UploadFile = File(None),
    cover_photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Construct update data
    update_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "bio": bio,
    }

    # Hash password only if provided
    if password:
        update_data["password"] = Hash.bcrypt(password)

    # Handle file uploads
    if profile_photo:
        profile_photo_path = await save_file(profile_photo, folder="profile_photos")
        update_data["profile_photo"] = profile_photo_path

    if cover_photo:
        cover_photo_path = await save_file(cover_photo, folder="cover_photos")
        update_data["cover_photo"] = cover_photo_path

    # Update the user in the database
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_query.update(update_data)
    db.commit()

    # Fetch the updated user data
    updated_user = user_query.first()

    return {
        "detail": "User profile updated successfully",
        "user": {
            "username": updated_user.username,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email,
            "profile_photo": updated_user.profile_photo,
            "cover_photo": updated_user.cover_photo,
            "bio": updated_user.bio,
        }
    }
