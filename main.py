from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine,Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
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

app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(movie_router)


Base.metadata.create_all(bind=engine)

        
@app.get('/',tags=['Home'])
def message():
    return HTMLResponse("<h1>Hello world</h1>")