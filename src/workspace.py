import cPickle as pickle
import numpy as np
import os
import scipy.stats as spstats

from models.movies import Movies
from models.ratings import Ratings
from models.users import Users


class Workspace(object):

    def __init__(self, movies, ratings, users):
        self.movies = movies
        self.ratings = ratings
        self.users = users

        self.summarize_movies()
        self.summarize_users()

    def summarize_movies(self):
        for m in self.movies.movies:
            movie_ratings = self.ratings.for_movie(m.ID)
            self.movies[m.ID].summarize(*Workspace.summary_stats(movie_ratings))

    def summarize_users(self):
        for u in self.users.users:
            movie_ratings = self.ratings.for_user(u.ID)
            self.users[u.ID].summarize(*Workspace.summary_stats(movie_ratings))

    @staticmethod
    def summary_stats(movie_ratings):
        r_ids = [r.ID for r in movie_ratings]
        count = len(movie_ratings)
        if count > 0:
            amean = np.mean([r.rating for r in movie_ratings])
            hmean = spstats.hmean([r.rating for r in movie_ratings])
            var = np.var([r.rating for r in movie_ratings])
        else:
            amean = np.NaN
            hmean = np.NaN
            var = np.NaN
        return r_ids, count, amean, hmean, var


def get_workspace(data_dir):

    cwd = data_dir
    pickle_fn = os.path.join(cwd, 'stats.pkl')

    if not os.path.isfile(pickle_fn):
        movies = Movies.parse_stream(open(os.path.join(cwd, 'movies.dat')))
        ratings = Ratings.parse_stream(open(os.path.join(cwd, 'ratings.dat')))
        users = Users.parse_stream(open(os.path.join(cwd, 'users.dat')))

        stats = Workspace(movies, ratings, users)
        pickle.dump(stats, open(pickle_fn, 'wb'))
    else:
        stats = pickle.load(open(pickle_fn))

    return stats

if __name__ == '__main__':
    get_workspace('dat/ml-1m')
