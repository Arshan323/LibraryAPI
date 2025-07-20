from fastapi import FastAPI
from models.models import Base
from router import router
from db import engine

app = FastAPI()
# ایجاد جداول
Base.metadata.create_all(bind=engine)

app.include_router(router=router.router,tags=['Basic'])
 