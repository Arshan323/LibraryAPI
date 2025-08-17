
import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()

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

