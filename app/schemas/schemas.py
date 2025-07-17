from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseUser):
    message: str

