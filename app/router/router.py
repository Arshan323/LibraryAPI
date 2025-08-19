from fastapi import APIRouter,Query,Depends, Form, HTTPException, status,Path,File, UploadFile
import bcrypt
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_


from middleware.bucket import upload_file
from middleware.auth_service import create_access_token,get_current_user,security

from Module_of_router import *

auth_router = APIRouter(
    prefix="/auth"
)

user_router = APIRouter(
    prefix="/user"
)

book_router = APIRouter(
    prefix="/book"
)

def check_role(role: str = Path(...), password_admin: str | None = Query(None)):
    if role.lower() == "admin" and password_admin != "1010":
        raise HTTPException(status_code=405, detail="Invalid admin password")
    return role

@auth_router.post("/signin", response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def signin(user_data: schemas.BaseUser,db: Session = Depends(get_db)):
    
    signin(user_data=user_data,db= db)
    return {
        "id": user_data.id,
        "username": user_data.username,
        "email": user_data.email,
        "message": "User created successfully"
    }

    

@auth_router.post("/login")
def login(user:schemas.login,db:Session=Depends(get_db)):
    token = login(user_data=user, db=db)
    return {"access_token": token}
   

@user_router.patch(
    path="/update/{user_id}",
    response_model=schemas.Update_Response,
    )
def update_user(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,user_data:schemas.Update,token:str = Depends(security),db:Session=Depends(get_db)):
    message = update_user(This_feature_Is_Only_For_The_Admin_To_Choose_Which_User_To_Edit=This_feature_is_only_for_the_admin_to_choose_which_user_to_edit,user_data=user_data, db=db, token=token)
    return message

        

@user_router.delete(
    path="/deleted",
    response_model=schemas.delete
)
def delete(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,token: str = Depends(security),db:Session=Depends(get_db)):
    delete_user(This_feature_Is_Only_For_The_Admin_To_Choose_Which_User_To_Edit=This_feature_is_only_for_the_admin_to_choose_which_user_to_edit, token=token, db=db)
    return {"message":"user deleted"}

    

@user_router.get("/search/",response_model=schemas.search)
def search(by_with: str, user: str, db: Session = Depends(get_db)):
    db = search(by_with=by_with, user=user, db=db)
    return db

@book_router.post("/upload", response_model=schemas.upload_book)
def upload_book(
    
    title: str = Form(...),  
    language: str = Form(...),
    page_counts: int = Form(...),
    pdf: UploadFile = File(...), 
    
    author: str | None = Form(None),
    genre: str | None = Form(None),  
    publisher: str | None = Form(None), 
    book_image: str | None = Form(None),  
    price: int | None = Form(None), 

    description: str | None = Form(None),
     
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    re = upload_book(
        title=title,
        author=author,
        genre=genre,
        language=language,
        page_counts=page_counts,
        pdf=pdf,
        book_image=book_image,
        price=price,
        publisher=publisher,
        description=description,
        user_id=token["user_id"],
        db=db
    )
    return re

@book_router.get("/get_your_book", response_model=schemas.get_book)
def get_your_book(token: str = Depends(security), db: Session = Depends(get_db)):
    try:
        token = get_current_user(token=token)

        book = db.query(models.Book).filter(models.Book.user_id == token["user_id"]).all()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
    
        return {
            "message": "Book retrieved successfully",
            "pdf": book
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@book_router.delete("/delete_book", response_model=schemas.delete_book)
def delete_book(book_id:int, token: str = Depends(security), db: Session = Depends(get_db)):
    delete_book(book_id=book_id, token=token, db=db)
    return {"message": "Book deleted successfully"}

@book_router.patch("/update_book", response_model=schemas.update_book)
def update_book(
    book_id:int,
    title: str | None = Form(None),  
    author: str | None = Form(None),
    genre: str | None = Form(None),  
    publisher: str | None = Form(None), 
    language: str | None = Form(None),  
    page_counts: str | None = Form(None), 
    book_image: str | None = Form(None),  
    price: str | None = Form(None), 
    pdf: UploadFile | None = UploadFile(None), 
    description: str | None = Form(None), 
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    update_book(title=title,book_id=book_id,author=author,genre=genre,publisher=publisher,language=language,page_counts=page_counts,book_image=book_image,price=price,pdf=pdf,db=db,token=token,description=description)
    return "Updated"
    
@book_router.get("/get_all_books", response_model=schemas.get_all_books)
def get_all_books(db: Session = Depends(get_db)):
    books = get_all_books(db=db)
    return {"message": "Books retrieved successfully", "books": books}

