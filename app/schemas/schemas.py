

from pydantic import BaseModel, EmailStr,Field,field_validator
from datetime import datetime
from typing import Optional
import re
# user_register
class BaseUser(BaseModel):
    username: str = Field(default="Your name", min_length=3, max_length=100)
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(default="Your password", min_length=6, max_length=100)
    @field_validator("username","email","password")
    @classmethod
    def check(cls, v):
        if not re.search(pattern=r"^[A-Za-z\u0622\u0627\u0628\u067E\u062A\u062B\u062C\u0686\u062D\u062E\u062F\u0632\u0631\u0632\u0698\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0641\u0642\u06A9\u06AF\u0644\u0645\u0646\u0648\u0647\u06CC]+$", string=v):
            raise ValueError("Invalid username")
        return v


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    message: str

    class Config:
        from_attributes = True

# login

class login(BaseModel):
    username: str = Field(default="Your name", min_length=3, max_length=100)
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(default="Your password", min_length=6, max_length=100)
    @field_validator("username","email","password")
    @classmethod
    def check(cls, v):
        if not re.search(pattern=r"^[A-Za-z\u0622\u0627\u0628\u067E\u062A\u062B\u062C\u0686\u062D\u062E\u062F\u0632\u0631\u0632\u0698\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0641\u0642\u06A9\u06AF\u0644\u0645\u0646\u0648\u0647\u06CC]+$", string=v):
            raise ValueError("Invalid username")
        return v


# update_user

class Update(BaseModel):
    username: str = Field(default="Your name", min_length=3, max_length=100)
    email: EmailStr = Field(min_length=5, max_length=100)
    password: str = Field(default="Your password", min_length=6, max_length=100)
    @field_validator("username","email","password")
    @classmethod
    def check(cls, v):
        if not re.search(pattern=r"^[A-Za-z\u0622\u0627\u0628\u067E\u062A\u062B\u062C\u0686\u062D\u062E\u062F\u0632\u0631\u0632\u0698\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0641\u0642\u06A9\u06AF\u0644\u0645\u0646\u0648\u0647\u06CC]+$", string=v):
            raise ValueError("Invalid username")
        return v

    
class Update_Response(BaseModel):
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


# delete book


class delete_book(BaseModel):
    message: str
    
# update_book
class update_book(BaseModel):
    message: str
    
# get_book

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


class get_book(BaseModel):
    message: str
    pdf: list[BookInfo]
    class Config:
        from_attributes = True



# get_all_books



class get_all_books(BaseModel):
    message: str
    books: list[BookInfo]
    class Config:
        from_attributes = True

