from models.movie import Movie as MovieModel

class MovieService():
    def __init__(self,db) -> None:
        self.db = db
        
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie(self,id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movie_by_category(self,category,year):
        result = self.db.query(MovieModel).filter(MovieModel.category == category, MovieModel.year == year).all()
        return result