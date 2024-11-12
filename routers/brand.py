
from fastapi import APIRouter
from .. import schemas, database, models
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
import uuid
from ..oauth2 import get_current_user
from .. import oauth2
get_db = database.get_db
router = APIRouter()

@router.post('/brandshow')
def create_brand(request: schemas.Brandshow, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    temp_id = UUID('4fa7e0e7-61fc-4553-88bf-17f253ac7e21')
    
    existing_brand = db.query(models.Brandshow).filter(models.Brandshow.Brand_Name == request.Brand_Name).first()
    if existing_brand:
        raise HTTPException(status_code=400, detail="A brand with this name already exists.")
    
    unique_slug = str(uuid.uuid4())  # Generates unique slug for each brand
    new_brand = models.Brandshow(
        user_id = current_user.id,
        Brand_Name=request.Brand_Name,
        Price=request.Price,
        slug=unique_slug,
        Brand_Tag=request.Brand_Tag,
        Brand_Description=request.Brand_Description,
        Brand_images=request.Brand_images,
        Brand_Industry=request.Brand_Industry,
        Brand_Categories=request.Brand_Categories
    ) 
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand
  
@router.get('/brandshow')
def BrandDisplay(db: Session=Depends(get_db)):
    brands = db.query(models.Brandshow).all()
    return brands
@router.get('/brandshow/{slug}', status_code=status.HTTP_200_OK) 
def BrandDetail(slug: str, response: Response,  db: Session=Depends(get_db)):
    brand = db.query(models.Brandshow).filter(models.Brandshow.slug  == slug ).first()
    if not brand: 
         response.status_code=status.HTTP_404_NOT_FOUND
         return {'detail':"Item not found"} 
    return brand

@router.put('/brandshow/{slug}', status_code=status.HTTP_202_ACCEPTED)
def update(slug: str, response: Response, request: schemas.Brandshow, db: Session=Depends(get_db)):
    brand = db.query(models.Brandshow).filter(models.Brandshow.slug == slug).update(request.model_dump())
    db.commit()
    if not brand:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': 'This Brand was not found '} 
    return {'detail': f'The Brand has been updated  '} 

@router.delete('/brandshow/{slug}', status_code=status.HTTP_200_OK)
def Delete_Brand(slug, db: Session=Depends(get_db)):
    brand = db.query(models.Brandshow).filter(models.Brandshow.slug == slug).delete(synchronize_session=False)
    return {'detail': 'The brand has been Deleted'}

