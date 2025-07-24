from fastapi import APIRouter,Depends, HTTPException,status,Path
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

router = APIRouter(
    prefix="/auth"
)

user_router = APIRouter(
    prefix="/get_user"
)

@router.post("/signup", response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def user_register(user_data: schemas.BaseUser, db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter(models.User.email==user_data.email).first():
            raise HTTPException(status_code=409,detail="email is already exist")

        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
        )
        hash_password = bcrypt.hashpw(password=user_data.password.encode(),salt=bcrypt.gensalt())
        new_user.password=hash_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "message": "User created successfully"
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="server error")
    


@user_router.get("/read/{user_id}",status_code=status.HTTP_200_OK)
def user(user_id:int=Path(ge=1), db: Session = Depends(get_db)):
    try:
    
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
        if not db_user:
            raise HTTPException(status_code=404,detail="User not found")
    
        return db_user
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")


@user_router.patch(
    path="/update/{user_id}",
    response_model=schemas.Update_Response
    )
def update_user(user_data:schemas.BaseUser,db:Session=Depends(get_db),user_id:int=Path(ge=1)):
    try:
        db_user = db.query(models.User).filter(models.User.id==user_id).first()
        if not db_user:
            raise HTTPException(status_code=404,detail="No user with id")
        db_user.username = user_data.username
        db_user.email = user_data.email
    
        hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())
        db_user.password = hashed_password
    
        db.commit()
        return {"message":"seccessful update","username":db_user.username,"email":db_user.email,"password":db_user.password,"id":db_user.id}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")
        

@user_router.delete(
    path="/deleted/{user_id}",
    response_model=schemas.delete
)
def delete(user_id:int=Path(ge=1),db:Session=Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.id==user_id).first()
        if not db_user:
            raise HTTPException(status_code=404,detail="No user with id")
        db.delete(db_user)
        db.commit()
        return {"message":"user deleted","user_id":db_user.id}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")
    

@user_router.get("/search/")
def search(by_with: str, user: str, db: Session = Depends(get_db)):
    try:
        if by_with.find("id") != -1:
            try:
                user_id = int(user)
            except Exception:
                raise HTTPException(status_code=400, detail="TypeError: id must be an integer")

            
            db_user = db.query(models.User).filter(models.User.id == user_id).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user


        elif by_with.find("email") != -1:
            
            db_user = db.query(models.User).filter(models.User.email == user).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user

        elif by_with.find("username") != -1:
            
            db_user = db.query(models.User).filter(models.User.username == user).first()
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user

        else:
            raise HTTPException(status_code=400, detail="Invalid search parameter")

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
