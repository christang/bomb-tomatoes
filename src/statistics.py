import cPickle as pickle
import numpy as np
import scipy.stats as spstats
import os

from models.movies import Movies
from models.ratings import Ratings
from models.users import Users


class Workspace(object):

    def __init__(self, movies, ratings, users):
        self.movies = movies
        self.ratings = ratings
        self.users = users

        self.movie_stats = self.summary_movies()
        self.user_stats = self.summary_users()

    def summary_movies(self):
        summary = {}

        for m in self.movies.movies:
            movie_ratings = self.ratings.for_movie(m.ID)
            summary[m.ID] = Workspace.summary_stats(movie_ratings)

        return summary

    def summary_users(self):
        summary = {}

        for u in self.users.users:
            movie_ratings = self.ratings.for_user(u.ID)
            summary[u.ID] = Workspace.summary_stats(movie_ratings)

        return summary

    @staticmethod
    def summary_stats(movie_ratings):
        count = len(movie_ratings)
        if count > 0:
            amean = np.mean([r.rating for r in movie_ratings])
            hmean = spstats.hmean([r.rating for r in movie_ratings])
            var = np.var([r.rating for r in movie_ratings])
        else:
            amean = np.NaN
            hmean = np.NaN
            var = np.NaN
        return count, amean, hmean, var


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
