from fastapi import APIRouter,status
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()
    
@user_router.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"message":"Unauthorized"})