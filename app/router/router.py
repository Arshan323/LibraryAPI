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
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "message": "User created successfully"
        }
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500,detail="server error")
    

@auth_router.post("/login/{user_id}&{role}")
def login(user:schemas.login,user_id:int,role: str=Depends(check_role),db:Session=Depends(get_db)):
    user_name = db.query(models.User).filter(models.User.id==user_id).first()

    if not user_name:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt.checkpw(user.password.encode('utf-8'), user_name.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user_id=user_id, role=role,username=user.username)
    return {"access_token": token}
   

@user_router.patch(
    path="/update/{user_id}",
    response_model=schemas.Update_Response,
    )
def update_user(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,user_data:schemas.Update,token:str = Depends(security),db:Session=Depends(get_db)):
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
        raise HTTPException(status_code=500,detail="server cant management")
        

@user_router.delete(
    path="/deleted/{user_id}/",
    response_model=schemas.delete
)
def delete(This_feature_is_only_for_the_admin_to_choose_which_user_to_edit:int,token: str = Depends(security),db:Session=Depends(get_db)):
    try:
        token = get_current_user(token=token)
 
        if token["role"] == "admin":
            db_user = db.query(models.User).filter(models.User.id==This_feature_is_only_for_the_admin_to_choose_which_user_to_edit).first()
        else:
            db_user = db.query(models.User).filter(models.User.id==token["user_id"]).first()
        
        db.delete(db_user)
        db.commit()
        return {"message":"user deleted","user_id":db_user.id}
    except SQLAlchemyError:
        raise HTTPException(status_code=500,detail="server cant management")
    

@user_router.get("/search/",response_model=schemas.search)
def search(by_with: str, user: str, db: Session = Depends(get_db)):
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
    
        return {"message": "Book deleted successfully"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
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

        return {"message": "Book updated successfully"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
@book_router.get("/get_all_books", response_model=schemas.get_all_books)
def get_all_books(db: Session = Depends(get_db)):
    try:
        books = db.query(models.Book).all()
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
    
        return {"message": "Books retrieved successfully", "books": books}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error")
