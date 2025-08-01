from fastapi import APIRouter,Query,Depends, Form, HTTPException, status,Path,Body,File, UploadFile
from streamlit import user
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
from middleware.bucket import upload_file
from middleware.auth_service import create_access_token

router = APIRouter(
    prefix="/auth"
)

user_router = APIRouter(
    prefix="/user"
)

book_router = APIRouter(
    prefix="/book"
)

@router.post("/signup", response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def user_register(user_data: schemas.BaseUser, db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter(models.User.email==user_data.email).first():
            raise HTTPException(status_code=409,detail="email is already exist")


        new_user = models.User(
            username=user_data.username,
            email=user_data.email
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
    

@router.post("/login")
def login():
    token = create_access_token(user_id=1, role="admin")
    return {"access_token": token}


@user_router.patch(
    path="/update/{user_id}",
    response_model=schemas.Update_Response,
    )
def update_user(user_data:schemas.Update,db:Session=Depends(get_db),user_id:int=Path(ge=1)):
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
    path="/deleted/{user_id}/",
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
    

@user_router.get("/search/",response_model=schemas.search)
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


@book_router.post("/upload", response_model=schemas.upload_book)
def upload_book(
    book_id: int,
    title: str = Form(...),  
    author: str | None = Form(None),
    genre: str | None = Form(None),  
    publisher: str | None = Form(None), 
    language: str = Form(...),  
    page_counts: str = Form(...), 
    book_image: str | None = Form(None),  
    price: str | None = Form(None), 
    pdf: str | None = Form(None), 
    description: str | None = Form(None), 
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


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
        link_download = pdf,
        book_image = book_image
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "file created",
        "pdf_url": pdf_url,
        "book_id": new_book.id
    }


@book_router.get("/get_book/{book_id}", response_model=schemas.get_book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {
        "message": "Book retrieved successfully",
        "pdf_url": book.link_download
    }
    

@book_router.delete("/delete_book/{book_id}", response_model=schemas.delete_book)
def delete_book(book:schemas.delete_book, book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")


    db.delete(book)
    db.commit()
    
    return {"message": "Book deleted successfully", "book_id": book_id}
@book_router.patch("/update_book/{book_id}/", response_model=schemas.update_book)
def update_book(
    book_id: int,
    title: str = Form(...),  
    author: str | None = Form(None),
    genre: str | None = Form(None),  
    publisher: str | None = Form(None), 
    language: str = Form(...),  
    page_counts: str = Form(...), 
    book_image: str | None = Form(None),  
    price: str | None = Form(None), 
    pdf: str | None = Form(None), 
    description: str | None = Form(None), 
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")



    book.name = title
    book.author = author
    book.genre = genre
    book.language = language
    book.page_counts = page_counts
    book.price = price
    book.publisher = publisher
    book.description = description
    book.link_download = pdf
    book.book_image = book_image

    db.commit()

@book_router.get("/get_all_books", response_model=schemas.get_all_books)
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    
    return {"message": "Books retrieved successfully", "books": books}

