from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from fastapi import UploadFile



class Blog(BaseModel):
    title: str
    body: str
    id: UUID
    
class Pitch(BaseModel):
    title: str
    Description: str
    Detail: str
    id: UUID
    Company: str

class Brandshow(BaseModel):
    Brand_Name: str
    Price: Optional[float] = None
    Brand_Tag: Optional[str] = None
    Brand_Description: Optional[str] = None
    Brand_images: Optional[List[str]] = None
    Brand_Industry: Optional[str] = None
    Brand_Categories: Optional[List[str]] = None



  
class UserCreation(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    bio: Optional[str] = None
    
class messageBase(BaseModel):
     body: str 
     id: UUID 
     
class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    bio: Optional[str] = None
    id: UUID
    pitches: List[Pitch]
    blogs: List[Blog]
    brands: List[Brandshow]
    messages: List[messageBase]
    
    

class showUser(BaseModel):
    username: str
    first_name: str
    email: str
    bio: Optional[str] = None
    last_name: Optional[str] = None
    id: UUID
   
    class Config():
        from_attributes = True 
        


class MessageDetail(BaseModel):
     body: str 
     id: UUID 
     user_id: showUser
     class config():
         from_attributes = True



class showPitch(Pitch):
    title: str
    Description: str
    Detail: str
    Company: str
    id: UUID
    user: showUser


class BlogCreate(BaseModel):
    title: str
    body: str
    images: Optional[List[UploadFile]] = []  # List of image files


    class Config:
        from_attributes = True
class ImageResponse(BaseModel):
    filename: str
    url: str
    
    @classmethod
    def from_model(cls, image):
        filename = image.path.split("/")[-1]
        url = f"/static/{image.path}"
        return cls(filename=filename, url=url)
           
class showBlog(Blog):
    title: str
    body: str
    author: showUser
    images: Optional[List[ImageResponse]] = []  # List of image files
    id: UUID
    class Config():
        from_attributes = True


class BrandDisplay(BaseModel):
    Brand_Name: str
    Price: Optional[float] = None
    Brand_Tag: Optional[str] = None
    Brand_Description: Optional[str] = None
    Brand_images: Optional[List[str]] = None
    Brand_Industry: Optional[str] = None
    Brand_Categories: Optional[List[str]] = None
    id: UUID
    user: showUser
    
    class Config():
        from_attributes = True

   


class login(BaseModel):
    username: str
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
