from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class Account(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Account_Create(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    published: bool
    owner: Account

class Post_Create(BaseModel):
    title: str
    content: str
    published: bool = True

class Post_Out(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_Data(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #type: ignore

