
import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# برای فایل‌های استاتیک (css, js, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# برای html
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
uvicorn_host = os.getenv("uvicorn_host",default="localhost")
uvicorn_port = os.getenv("uvicorn_port",default="8000")
env = os.getenv("env",default="dev")

if __name__ == "__main__":
    uvicorn.run(
        app = "config:app",
        host=uvicorn_host,
        port=int(uvicorn_port),
        reload=True if env=="dev" else False
    )

