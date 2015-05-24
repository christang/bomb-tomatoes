import os

from lib.workspace import Workspace
from models.movies import Movies
from models.ratings import Ratings
from models.users import Users


def load_data(data_dir, with_components=True):
    users = Users.parse_stream(open(os.path.join(data_dir, 'users.dat')))
    movies = Movies.parse_stream(open(os.path.join(data_dir, 'movies.dat')))
    ratings = Ratings.parse_stream(open(os.path.join(data_dir, 'ratings.dat')))

    w = Workspace(movies, ratings, users)
    w.summarize_users()
    w.summarize_movies()
    if with_components:
        w.extract_components()
    return users, movies, ratings
