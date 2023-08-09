from fastapi import FastAPI,Body
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

@app.post('/movies',tags=['Movies'])
def create_movie(id:int = Body(),title:str = Body(),overview:str = Body(),year:int = Body(),rating:float = Body(),category:str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating':rating,
        'category': category 
    })
    return movies

@app.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int,title:str = Body(),overview:str = Body(),year:int = Body(),rating:float = Body(),category:str = Body()):
    movie = list(filter(lambda m: m['id'] == id,movies))
        
    if movie[0] in movies:
        movies[movie.index(movie[0])]['title'] = title
        movies[movie.index(movie[0])]['overview'] = overview
        movies[movie.index(movie[0])]['year'] = year
        movies[movie.index(movie[0])]['rating'] = rating
        movies[movie.index(movie[0])]['category'] = category
    return movies

@app.delete('/movies/{id}',tags=['Movies'])
def delete_movie(id:int):
    movie = list(filter(lambda m: m['id'] == id,movies))
    
    if movie[0] in movies:
        del movies[movie.index(movie[0])]
    
    return movies