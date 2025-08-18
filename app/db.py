from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER_NAME = os.getenv("DB_USER_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST_NAME = os.getenv("DB_HOST_NAME")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


DB_Url = f"postgresql+psycopg2://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DB_Url)

session_local = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
