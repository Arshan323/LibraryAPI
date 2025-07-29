

from fastapi import Form,File, UploadFile
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
# user_register
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True

# update_user

class Update(BaseModel):
    username: str
    email: EmailStr
    password: str
    previous_password: str
    
class Update_Response(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    message: str

    class Config:
        from_attributes = True


# delete
class delete(BaseModel):
    message:str
    user_id:int
    
# search
class search(BaseModel):
    	
    id:int
    email: EmailStr
    phone_number: Optional[str]
    update_at: datetime
    username: str
    created_at: datetime
    
# upload_book

class upload_book(BaseModel):
    message:str
    pdf_url:str
    book_id:int

# delete book
class delete_book(BaseModel):
    message: str
    book_id: int
    
# update_book
class update_book(BaseModel):
    message: str
    
# get_book
class get_book(BaseModel):
    message: str
    pdf_url: str




# get_all_books

class BookInfo(BaseModel):
    id: int
    name: str
    author: str
    genre: str
    language: str
    page_counts: int
    price: int
    link_download: str

    class Config:
        from_attributes = True


class get_all_books(BaseModel):
    message: str
    books: list[BookInfo]
    class Config:
        from_attributes = True

