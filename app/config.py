from fastapi import FastAPI
from models.models import Base
from router import router
from db import engine

app = FastAPI(
    title="LIBRARYAPI"
)
# ایجاد جداول
Base.metadata.create_all(bind=engine)

app.include_router(router=router.auth_router,tags=["auth"])

app.include_router(router=router.user_router,tags=["user"])

app.include_router(router=router.book_router,tags=["book"])




