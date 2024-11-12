from typing import Self, Optional, List
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID


from . import schemas, models
from .database import engine, get_db
from sqlalchemy.orm import Session   
from fastapi import Depends, status, Response, HTTPException
from slugify import slugify
import uuid
from .routers import authentication, blog, user, pitch, brand, message, myprofile
app = FastAPI()
from .models import Blog, SQLModel
UPLOAD_DIR = "images"

# Create database tables 
""" models.Base.metadata.create_all(engine) """

SQLModel.metadata.create_all(bind=engine)
""" # Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
 """
from fastapi.middleware.cors import CORSMiddleware

# Define allowed origins, which are the URLs of your frontend application(s)
origins = [
    "http://localhost:3000",   # For local Nuxt development
    "https://your-production-domain.com"  # Replace with your production domain if needed
]

# Add the CORS middleware to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # allows only the specified origins
    allow_credentials=True,            # allows cookies, etc.
    allow_methods=["*"],               # allows all HTTP methods like GET, POST
    allow_headers=["*"],               # allows all headers to be sent
)

app.include_router(myprofile.router, tags=['My Profile'])
app.include_router(authentication.router, tags=['Authentication'])
app.include_router(blog.router, tags=['Blogs'])
app.include_router(user.router, tags=[' User'])
app.include_router(pitch.router, tags=['Pitch'])
app.include_router(brand.router, tags=['Brands'])
app.include_router(message.router, tags=['Messaging'])



 


    