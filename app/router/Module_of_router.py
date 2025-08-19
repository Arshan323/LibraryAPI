
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

def signin(user_data,db):
    try:
        if db.query(models.User).filter(models.User.email==user_data.email).first():
            raise HTTPException(status_code=409,detail="email is already exist")



        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            role=user_data.role
        )
        hash_password = bcrypt.hashpw(password=user_data.password.encode(),salt=bcrypt.gensalt())
        new_user.password=hash_password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="server error")
    


def login(user_data, db):
    try:
        db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not bcrypt.checkpw(user_data.password.encode(), db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(user_id=db_user.id, role=db_user.role, username=db_user.username)
        return {token}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="server error")
    

def update_user(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit,user_data, db, token):
    try:
        token = get_current_user(token=token)


        if token["role"] == "admin":
            db_user = db.query(models.User).filter(models.User.id==This_feature_is_only_for_the_admin_to_choose_which_user_to_edit).first()
        else:
            db_user = db.query(models.User).filter(models.User.id==token["user_id"]).first()

        db_user.username = user_data.username
        db_user.email = user_data.email
    
        hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())
        db_user.password = hashed_password
    
        db.commit()
        return {"message":"seccessful update","username":db_user.username,"email":db_user.email,"password":db_user.password,"id":db_user.id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="server error")
    
    
    
def delete_user(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit,db, token):
    try:
        token = get_current_user(token=token)
 
        if token["role"] == "admin":
            db_user = db.query(models.User).filter(models.User.id==This_feature_is_only_for_the_admin_to_choose_which_user_to_edit).first()
        else:
            db_user = db.query(models.User).filter(models.User.id==token["user_id"]).first()
        

        db.delete(db_user)
        db.commit()
        return {"message":"user deleted"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")


def search(by_with, user, db):
    try:


        if by_with.find("email") != -1:
            
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
    db: Session = Depends(get_db)):
    try:
        token = get_current_user(token=token)



        pdf_url = upload_file(pdf, f"test/{title}.pdf")

        new_book = models.Book(
            name = title,
            author = author,
            genre = genre,
            language = language,
            page_counts = page_counts,
            price = price,
            publisher = publisher,
            description = description,
            link_download = pdf_url,
            book_image = book_image,
            user_id = token["user_id"]
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {
            "message": "file created",
            "pdf_url": pdf_url,
            "book_id": new_book.id
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
def delete_book(book_id, token, db):
    try:
        token = get_current_user(token=token)
        if token["role"] == "admin":
            book = db.query(models.Book).filter(models.Book.id == book_id).first()
        else:
            book = db.query(models.Book).filter(and_(models.Book.id == book_id, models.Book.user_id == token["user_id"])).first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(book)
        db.commit()

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
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
    db: Session = Depends(get_db)):
    try:
        token = get_current_user(token=token)
        if token["role"] == "admin":
            book = db.query(models.Book).filter(models.Book.id == book_id).first()
        else:
            book = db.query(models.Book).filter(and_(models.Book.id == book_id, models.Book.user_id == token["user_id"])).first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if title:
            book.name = title
        if author:
            book.author = author
        if genre:
            book.genre = genre
        if language:
            book.language = language
        if page_counts:
            book.page_counts = page_counts
        if price:
            book.price = price
        if publisher:
            book.publisher = publisher
        if description:
            book.description = description
        if pdf:
            book.link_download = pdf
        if book_image:
            book.book_image = book_image

        db.commit()


    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
def get_all_books(db):    
    try:
        books = db.query(models.Book).all()
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
    
    