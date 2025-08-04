from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime,LargeBinary
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(LargeBinary(1500), nullable=False)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    books = relationship("Book", back_populates="owner")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author = Column(String)
    genre = Column(String)
    publisher = Column(String)
    language = Column(String)
    page_counts = Column(Integer)
    book_image = Column(String)
    price = Column(Float,nullable=True)
    link_download = Column(String)
    description = Column(Text)
    role = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="books")


