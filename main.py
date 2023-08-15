from fastapi import FastAPI,Depends,Body,HTTPException,Path,Query,status,Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from typing import Any, Coroutine, Optional,List
#from starlette.requests import Request
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2023,
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

app = FastAPI()
#change the name app
app.title = "My first app in FastAPI"
#change version
app.version = "0.0.1"
#tags for group routes

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403,detail="Invalid Credentials")


class User(BaseModel):
    email:str
    password:str
    
class Movie(BaseModel):
    id:Optional[int] = Field(default=None)
    title:str = Field(min_length=5,max_length=15)
    overview:str = Field(min_length=15,max_length=50)
    year:int = Field(le=2023)
    rating:float = Field(ge=1,le=10)
    category:str = Field(min_length=5,max_length=15)
    
    class Config:
        json_schema_extra = {
            "example":{
                'id': 1,
                'title': 'My movie',
                'overview': "En un exuberante",
                'year': 2023,
                'rating': 7.8,
                'category': 'Acción',  
            }
        }
    
@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h1>Hello world</h1>")

@app.post('/login',tags=['auth'])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,content={"message":"Unauthorized"})

#all movies
@app.get('/movies',tags=['Movies'],response_model=List[Movie],status_code=status.HTTP_200_OK,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#url parameter
@app.get('/movies/{id}',tags=['Movies'],response_model=Movie,status_code=200)
def get_movie(id:int = Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=400,content={"message":"Movie not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#query parameters
@app.get('/movies/',tags=['Movies'],response_model=List[Movie],status_code=200)
def get_movie_by_category(category:str = Query(min_length=5,max_length=15),year:int = Query(le=2023)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category, MovieModel.year == year).all()
    if not result:
         return JSONResponse(status_code=400,content={"message":"Movie not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.post('/movies',tags=['Movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Movie created successfully"})

@app.put('/movies/{id}',tags=['Movies'],response_model=dict,status_code=200)
def update_movie(id:int,movie:Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=400,content={"message":"Movie not found"})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200,content={"message":"Movie updated successfully"})

@app.delete('/movies/{id}',tags=['Movies'],response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=400,content={"message":"Movie not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message":"Movie deleted successfully"})