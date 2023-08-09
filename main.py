from fastapi import FastAPI,Body,Path,Query
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional,List

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

#all movies
@app.get('/movies',tags=['Movies'],response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

#url parameter
@app.get('/movies/{id}',tags=['Movies'],response_model=Movie)
def get_movie(id:int = Path(ge=1,le=2000)) -> Movie:
    return JSONResponse(content=[movie for movie in movies if movie['id'] == id])

#query parameters
@app.get('/movies/',tags=['Movies'],response_model=List[Movie])
def get_movie_by_category(category:str = Query(min_length=5,max_length=15),year:str = Query(le=2023)) -> List[Movie]:
    return JSONResponse(content=[movie for movie in movies if (movie['category'] == category and movie['year'] == year)])

@app.post('/movies',tags=['Movies'],response_model=dict)
def create_movie(movie:Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message":"Movie created successfully"})

@app.put('/movies/{id}',tags=['Movies'],response_model=dict)
def update_movie(id:int,movie:Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={"message":"Movie updated successfully"})
    return JSONResponse(content={"message":"Error"})

@app.delete('/movies/{id}',tags=['Movies'],response_model=dict)
def delete_movie(id:int) -> dict:
    for movie in movies:
    
        if movie['id'] == id:
            movies.remove(movie)
    
            return JSONResponse(content={"message":"Movie deleted successfully"})
    
    return JSONResponse(content={"message":"Error"})