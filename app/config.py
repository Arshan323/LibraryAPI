from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import asc, desc
from db import engine, get_db
from models.models import Base, User as UserModel
from schemas.schemas import BaseUser, User

app = FastAPI()

# ایجاد جداول
Base.metadata.create_all(bind=engine)

@app.get("/")
def welcome() -> str:
    return "welcome"

@app.post("/signup", response_model=User)
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
    
    return User(username=new_user.username, email=new_user.email, message="User registered successfully")



@app.get("/users", response_model=List[User])
def get_users(
    sort_by_created_at: Optional[bool] = Query(None),
    limit: Optional[int] = Query(None),
    search_email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(UserModel)
    
    if search_email:
        query = query.filter(UserModel.email == search_email)
    
    if sort_by_created_at is not None:
        order = asc(UserModel.created_at) if sort_by_created_at else desc(UserModel.created_at)
        query = query.order_by(order)
    
    if limit:
        query = query.limit(limit)
    
    return query.all()
