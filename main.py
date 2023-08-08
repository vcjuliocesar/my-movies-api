from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
    
    movie = list(filter(lambda m: m['id'] == id,movies))
    
    return movie[0] if len(movie) > 0 else []

#query parameters
@app.get('/movies/',tags=['Movies'])
def get_movie_by_category(category:str,year:str):
    return [movie for movie in movies if (movie['category'] == category and movie['year'] == year)]
     