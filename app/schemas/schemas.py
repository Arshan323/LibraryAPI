

from pydantic import BaseModel, EmailStr

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