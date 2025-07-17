from fastapi import APIRouter,Depends, HTTPException
from models.models import User as UserModel
from schemas.schemas import BaseUser, User
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()

@router.get("/")
def welcome() -> str:
    return "welcome"

@router.post("/signup", response_model=User)
def user_register(user_credentials: BaseUser, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if existing_user: 
        raise HTTPException(status_code=409, detail="Email already registered")
    
    new_user = UserModel(
        username=user_credentials.username,
        email=user_credentials.email,
        hashed_password=user_credentials.password  # باید هش شود
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"username":new_user.username,"email":new_user.email,"password":new_user.hashed_password,"message":"sucessfull"}



@router.get("/users/")
def read_users(db:Session=Depends(get_db)):
    all_user = db.query(UserModel).all()
    if all_user:
        return "NO user"
    return all_user