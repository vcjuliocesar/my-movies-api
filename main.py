from fastapi import FastAPI,Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2023',
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
    id:Optional[int] = None
    title: str
    overview: str
    year: int
    rating:float
    category: str 
    
@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h1>Hello world</h1>")

#all movies
@app.get('/movies',tags=['Movies'])
def get_movies():
    return movies

#url parameter
@app.get('/movies/{id}',tags=['Movies'])
def get_movie(id:int):
    return [movie for movie in movies if movie['id'] == id]

#query parameters
@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str,year:str):
    return [movie for movie in movies if (movie['category'] == category and movie['year'] == year)]

@app.post('/movies',tags=['Movies'])
def create_movie(movie:Movie):
    movies.append(movie)
    return movies

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int,movie:Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return movies

@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int):
    for movie in movies:
    
        if movie['id'] == id:
            movies.remove(movie)
    
    return movies