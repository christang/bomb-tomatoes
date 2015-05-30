import numpy as np
import os
import scipy.stats as spstats

from lib.cache import Pickled
from models.movies import Movies
from models.ratings import Ratings
from models.users import Users


class Workspace(Pickled):

    def __init__(self, movies, ratings, users):
        super(Workspace, self).__init__()

        self.movies = movies
        self.ratings = ratings
        self.users = users
        self.tags = {}
        self.decades = {}
        self.age_groups = {}
        self.genders = {}
        self.occupations = {}

    def summarize_movies(self):
        def compute():
            movie_ratings = self.ratings.for_movie(m.ID)
            return Workspace.summary_stats(movie_ratings)

        for m in self.movies.movies:
            pickle_fn = os.path.join(self.cwd, 'movies', str(m.ID))
            self.movies[m.ID].summarize(*Pickled.load_or_compute(pickle_fn, compute))

    def summarize_users(self):
        def compute():
            movie_ratings = self.ratings.for_user(u.ID)
            return Workspace.summary_stats(movie_ratings)

        for u in self.users.users:
            pickle_fn = os.path.join(self.cwd, 'users', str(u.ID))
            self.users[u.ID].summarize(*Pickled.load_or_compute(pickle_fn, compute))

    def summarize_tags(self):
        def compute():
            movie_ratings = self.ratings.for_tag(t, movies=self.movies)
            return Workspace.summary_stats(movie_ratings)

        for t in self.movies.tags:
            pickle_fn = os.path.join(self.cwd, 'tags', str(t))
            self.tags[t] = Pickled.load_or_compute(pickle_fn, compute)

    def summarize_decades(self):
        def compute():
            movie_ratings = self.ratings.for_decade(d, movies=self.movies)
            return Workspace.summary_stats(movie_ratings)

        for d in self.movies.decades:
            pickle_fn = os.path.join(self.cwd, 'decades', str(d))
            self.decades[d] = Pickled.load_or_compute(pickle_fn, compute)

    def summarize_age_groups(self):
        def compute():
            movie_ratings = self.ratings.for_age_group(a, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for a in self.users.age_groups:
            pickle_fn = os.path.join(self.cwd, 'age_groups', str(a))
            self.age_groups[a] = Pickled.load_or_compute(pickle_fn, compute)

    def summarize_genders(self):
        def compute():
            movie_ratings = self.ratings.for_gender(g, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for g in self.users.genders:
            pickle_fn = os.path.join(self.cwd, 'genders', str(g))
            self.genders[g] = Pickled.load_or_compute(pickle_fn, compute)

    def summarize_occupations(self):
        def compute():
            movie_ratings = self.ratings.for_occupation(o, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for o in self.users.occupations:
            pickle_fn = os.path.join(self.cwd, 'occupations', str(o))
            self.occupations[o] = Pickled.load_or_compute(pickle_fn, compute)

    def extract_components(self, split):
        def compute():
            raise Exception('run features.py to extract components')

        for m in self.movies.movies:
            if m.count > 0:
                pickle_fn = os.path.join(self.cwd, 'components', '%02d' % split, str(m.ID))
                components = Pickled.load_or_compute(pickle_fn, compute)
                self.movies[m.ID].components = np.ones(components.size + 1)
                self.movies[m.ID].components[1:] = components  # components[0] === scale factor

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


def load_data(data_dir):
    users = Users.parse_stream(open(os.path.join(data_dir, 'users.dat')))
    movies = Movies.parse_stream(open(os.path.join(data_dir, 'movies.dat')))
    ratings = Ratings.parse_stream(open(os.path.join(data_dir, 'ratings.dat')))

    w = Workspace(movies, ratings, users)
    w.summarize_users()
    w.summarize_movies()
    return w
