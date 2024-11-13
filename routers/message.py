
from fastapi import APIRouter
import schemas, database, models
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlalchemy.orm import Session   
from uuid import UUID

get_db = database.get_db
router = APIRouter()

@router.post('/message')
def create_message(id: UUID, request: schemas.messageBase, db: Session=Depends(get_db)):
    temp_id = UUID('4fa7e0e7-61fc-4553-88bf-17f253ac7e21')
    message = models.Message(body=request.body, user_id = temp_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    
@router.get('/message')
def all_messages(db: Session =Depends(get_db)):
    all = db.query(models.Message).all()
    return all

@router.get('/message/{id}')
def message_detail(id: UUID, response_model=schemas.MessageDetail,db: Session = Depends(get_db)):
    messageDetail = db.query(models.Message).filter(models.Message.id==id).first()
    return messageDetail 

@router.delete('/message/{id}')
def deleteMessage(id: UUID, db:Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == id).delete(synchronize_session=False)
    return {'detail': 'message deleted'}