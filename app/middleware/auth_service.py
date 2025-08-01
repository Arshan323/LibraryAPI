from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
import jwt
from datetime import datetime, timedelta


security = HTTPBearer()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# -------------------------------
# Create JWT Token
# -------------------------------
def create_access_token(user_id: int, role: str):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
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

# -------------------------------
# Routes
# -------------------------------
# # @app.post("/login")
# def login():
#     # Dummy login
#     token = create_access_token(user_id=1, role="admin")
#     return {"access_token": token}

# @app.get("/protected")
# def protected_route(current_user: dict = Depends(get_current_user)):
#     return {
#         "message": "Access granted",
#         "user_id": current_user["user_id"],
#         "role": current_user["role"]
#     }









