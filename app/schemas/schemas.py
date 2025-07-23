

from pydantic import BaseModel, EmailStr

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


class Update_Response(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    message: str

    class Config:
        orm_mode = True
