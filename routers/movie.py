from fastapi import APIRouter
from fastapi import Depends,Path,Query,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

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

#all movies
@movie_router.get('/movies',tags=['Movies'],response_model=List[Movie],status_code=status.HTTP_200_OK,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies() #db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#url parameter
@movie_router.get('/movies/{id}',tags=['Movies'],response_model=Movie,status_code=200)
def get_movie(id:int = Path(ge=1,le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=400,content={"message":"Movie not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#query parameters
@movie_router.get('/movies/',tags=['Movies'],response_model=List[Movie],status_code=200)
def get_movie_by_category(category:str = Query(min_length=5,max_length=15),year:int = Query(le=2023)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category,year)
    if not result:
         return JSONResponse(status_code=400,content={"message":"Movie not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.post('/movies',tags=['Movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Movie created successfully"})

@movie_router.put('/movies/{id}',tags=['Movies'],response_model=dict,status_code=200)
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

@movie_router.delete('/movies/{id}',tags=['Movies'],response_model=dict,status_code=200)
def delete_movie(id:int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=400,content={"message":"Movie not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content={"message":"Movie deleted successfully"})