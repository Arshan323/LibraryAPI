from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("Secret_key")
ALGORITHM = os.getenv("Algorithm")
Time = 1
# -------------------------------
# Create JWT Token
# -------------------------------
def create_access_token(user_id: int, role: str):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=Time)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# -------------------------------
# Dependency: Verify JWT
# -------------------------------
def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload.get("user_id"), "role": payload.get("role")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



# @app.get("/protected")
# def protected_route(current_user: dict = Depends(get_current_user)):
#     return {
#         "message": "Access granted",
#         "user_id": current_user["user_id"],
#         "role": current_user["role"],
#         "username": current_user.get("username")
#     }









