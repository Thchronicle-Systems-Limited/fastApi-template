from fastapi import APIRouter
from .. import schemas, database, models
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID
from ..oauth2 import get_current_user
from .. import oauth2
get_db = database.get_db
router = APIRouter()



@router.post('/pitch', status_code=status.HTTP_201_CREATED) 
def createpitch(request: schemas.Pitch, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_pitch = models.Pitch(title=request.title, Description=request.Description, Detail=request.Detail, Company=request.Company, user_id = current_user.id) 
    db.add(new_pitch)
    db.commit() 
    db.refresh(new_pitch)
    return new_pitch 

@router.get('/pitch')
def get_pitch(db: Session=Depends(get_db)):
    pitches = db.query(models.Pitch).all()
    return pitches 

@router.get('/pitch/{id}', response_model=schemas.showPitch,status_code=status.HTTP_200_OK) 
def getPitch(id: UUID, response: Response, db:Session= Depends(get_db)):
    pitch = db.query(models.Pitch).filter(models.Pitch.id == id).first()
    if not pitch:
        response.status_code=status.HTTP_404_NOT_FOUND 
        return {'detail': f'The pitch with the id {id} was not found '}
    user = db.query(models.User).filter(models.User.id == pitch.user_id).first()
    return schemas.showPitch(
    id=pitch.id,
    title=pitch.title,
    Description=pitch.Description,  # Make sure to match case here
    Detail=pitch.Detail,            # Match case
    Company=pitch.Company,          # Match case
    user=schemas.showUser(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        email=user.email,
        last_name=user.last_name
    )
)

 
@router.delete('/pitch/{id}', status_code=status.HTTP_200_OK)
def destroy(id, response: Response, db: Session = Depends(get_db)):
    pitch = db.query(models.Pitch).filter(models.Pitch.id == id).delete(synchronize_session=False)
    db.commit()
    if not pitch:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'The Pitch id with {id} does not exist'}
    return {'detail': f'The pitch with Id {id} was deleted'} 

@router.put('/pitch/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Pitch, response: Response, db:Session=Depends(get_db)):
    pitch = db.query(models.Pitch).filter(models.Pitch.id == id).update(request.model_dump())
    db.commit()
    if not pitch:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'the pitch with the Id {id} was not found'}
    return 'The pitch was updated successfully' 
    