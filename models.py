""" from sqlalchemy import Column, Integer, String, ARRAY, Float, JSON, ForeignKey, Table, DateTime
from . database import Base
from datetime import datetime
from fastapi import File, UploadFile
from typing import List
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID
import uuid

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(Base, TimestampMixin):
    __tablename__ = "Users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    bio = Column(String)
    profile_photo = Column(String)
    cover_photo = Column(String)
    blogs = relationship('Blog', back_populates='author')
    pitches = relationship('Pitch', back_populates='pitcher')
    brands = relationship('Brandshow', back_populates='brand_founder')
    messages = relationship('Message', back_populates='sender')
    

class Message(Base, TimestampMixin):
    __tablename__ = 'messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    sender = relationship('User', back_populates='messages')
   
 
class Blog(Base, TimestampMixin):
    __tablename__ = "blogs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    author = relationship('User', back_populates='blogs')
    images = relationship("BlogImage", back_populates="blog", cascade="all, delete")


class BlogImage(Base):
    __tablename__ = "blogimages"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    blog = relationship("Blog", back_populates="images")
    def __repr__(self):
        return f"<Image(id={self.id}, path={self.path})>"
        

class Pitch(Base, TimestampMixin):
    __tablename__ = "pitches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    Description = Column(String)
    Detail = Column(String)
    Company = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    pitcher = relationship('User', back_populates='pitches')
     

class Brandshow(Base, TimestampMixin):
    __tablename__ = 'Brand_sales'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Brand_Name = Column(String, nullable=False, unique=True)
    slug = Column(String, unique=True, index=True)
    Price = Column(Float, nullable=True)
    Brand_Tag = Column(String, nullable=True)
    Brand_Description = Column(String, nullable=True)
    Brand_images = Column(JSON, nullable=True)  # Ensure JSON structure
    Brand_Industry = Column(String, nullable=True)
    Brand_Categories = Column(JSON, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    brand_founder = relationship('User', back_populates='brands')
    
    
 """
 
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID
from sqlalchemy import Column
from sqlalchemy.types import JSON

class User(SQLModel, table=True):
    __tablename__ = "Users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    bio: Optional[str] = None
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationships
    blogs: List["Blog"] = Relationship(back_populates="author")
    pitches: List["Pitch"] = Relationship(back_populates="pitcher")
    brands: List["Brandshow"] = Relationship(back_populates="brand_founder")
    messages: List["Message"] = Relationship(back_populates="sender")

class Message(SQLModel, table=True):
    __tablename__ = 'messages'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    body: str
    user_id: UUID = Field(foreign_key='Users.id', nullable=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    sender: "User" = Relationship(back_populates="messages")

class Blog(SQLModel, table=True):
    __tablename__ = "blogs"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str
    body: str
    user_id: UUID = Field(foreign_key='Users.id', nullable=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    author: "User" = Relationship(back_populates="blogs")
    images: List["BlogImage"] = Relationship(back_populates="blog", sa_relationship_kwargs={"cascade": "all, delete"})

class BlogImage(SQLModel, table=True):
    __tablename__ = "blogimages"
    id: int = Field(default=None, primary_key=True)
    path: str
    blog_id: UUID = Field(foreign_key="blogs.id")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
     
    # Relationships
    blog: "Blog" = Relationship(back_populates="images")
    
    def __repr__(self):
        return f"<Image(id={self.id}, path={self.path})>"

class Pitch(SQLModel, table=True):
    __tablename__ = "pitches"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    Description: str
    Detail: str
    Company: str
    user_id: UUID = Field(foreign_key='Users.id', nullable=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    pitcher: "User" = Relationship(back_populates="pitches")



class Brandshow(SQLModel, table=True):
    __tablename__ = 'Brand_sales'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    Brand_Name: str = Field(nullable=False, unique=True)
    slug: str = Field(unique=True, index=True)
    Price: Optional[float] = None
    Brand_Tag: Optional[str] = None
    Brand_Description: Optional[str] = None
    Brand_Industry: Optional[str] = None
    Brand_Categories: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    user_id: UUID = Field(foreign_key='Users.id', nullable=False)
    images: List["BrandImage"] = Relationship(back_populates="brand", sa_relationship_kwargs={"cascade": "all, delete"})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    brand_founder: "User" = Relationship(back_populates="brands")

class BrandImage(SQLModel, table=True):
    __tablename__ = "brandimages"
    id: int = Field(default=None, primary_key=True)
    path: str
    brand_id: UUID = Field(foreign_key="Brand_sales.id")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    brand: "Brandshow" = Relationship(back_populates="images")
    
    def __repr__(self):
        return f"<Image(id={self.id}, path={self.path})>"