from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class User(BaseUser):
    message: str

