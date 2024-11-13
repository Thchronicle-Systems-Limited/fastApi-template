
from fastapi import APIRouter, UploadFile, File
import schemas, database, models, oauth2
from typing import List, Optional
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
from  oauth2 import get_current_user
import oauth2
import uuid
from io import BytesIO
from PIL import Image  # To handle image processing
import shutil
import os

get_db = database.get_db
router = APIRouter()

UPLOAD_DIR = "uploads/"

@router.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.showBlog)
async def create_blog(
    title: str,
    body: str,
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    # Create the blog post entry
    new_blog = models.Blog(title=title, body=body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    image_paths = []

    # Handle image uploads
    if images:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        for image in images:
            # Validate image type
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

            # Generate unique filename
            filename = f"{uuid.uuid4().hex}_{image.filename}"
            filepath = os.path.join(UPLOAD_DIR, filename)

            # Save image to disk
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            # Convert UUID to string before saving to database
            new_image = models.BlogImage(path=filepath, blog_id=str(new_blog.id))
            db.add(new_image)
            image_paths.append({"filename": filename, "url": filepath})

        db.commit()  # Ensure changes are committed

    # Fetch images from the database
    images = db.query(models.BlogImage).filter(models.BlogImage.blog_id == str(new_blog.id)).all()

    # Prepare image paths for response
    image_response = [{"filename": img.path.split('/')[-1], "url": img.path} for img in images]

    # Prepare user data for response
    user_data = {
        "id": str(current_user.id),
        "username": current_user.username,
        "first_name": current_user.first_name,
        "email": current_user.email,
    }

    # Response data
    return {
        "id": str(new_blog.id),
        "title": new_blog.title,
        "body": new_blog.body,
        "user": user_data,
        "images": image_response,
    }

@router.get('/blog')
def get_blog(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs



""" @router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.showBlog)
def showblog(id: UUID, response: Response, db: Session = Depends(get_db), current_user: schemas.showUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog: 
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'The blog post with the id {id} was not found'}
    # Fetch the user info to include in the response
    user = db.query(models.User).filter(models.User.id == blog.user_id).first()
    return schemas.showBlog(id=blog.id, title=blog.title, body=blog.body, user=schemas.showUser(id=user.id, username=user.username, first_name=user.first_name, email=user.email, last_name =user.last_name ))
 """
 
from sqlalchemy.orm import joinedload

from sqlalchemy.orm import joinedload

@router.get('/blog/{id}', response_model=schemas.showBlog)
def Get_Blog_Detail(id: str, db: Session = Depends(get_db)):
    blog = (
        db.query(models.Blog)
        .options(
            joinedload(models.Blog.author),
            joinedload(models.Blog.images)
        )
        .filter(models.Blog.id == id)
        .first()
    )

    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Transform image data
    images = [
        schemas.ImageResponse(
            filename=image.path.split("/")[-1],
            url=f"/static/{image.path}"
        )
        for image in blog.images
    ]

    # Construct the response dictionary explicitly
    response_data = {
        "title": blog.title,
        "body": blog.body,
        "author": blog.author,
        "images": images,
        "id": blog.id,
    }

    return response_data



@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False) 
    db.commit() 
    return 'Done'
 
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.BlogCreate, response: Response, db: Session=Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)): 
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request.model_dump())  
    db.commit()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'The blog content with Id {id} was not found'}
    return 'Updated successfully' 
   