

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
        orm_mode = True

# update_user

class Update_Response(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    message: str

    class Config:
        orm_mode = True


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
