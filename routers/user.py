from fastapi import APIRouter
from fastapi import status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email:str
    password:str
    
@user_router.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"message":"Unauthorized"})