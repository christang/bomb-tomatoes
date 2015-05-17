import cPickle
import numpy as np
import os
import scipy.stats as spstats


class Workspace(object):

    def __init__(self, movies, ratings, users, cwd='dat/pkl'):
        self.cwd = cwd

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
            self.movies[m.ID].summarize(*Workspace.load_or_compute(pickle_fn, compute))

    def summarize_users(self):
        def compute():
            movie_ratings = self.ratings.for_user(u.ID)
            return Workspace.summary_stats(movie_ratings)

        for u in self.users.users:
            pickle_fn = os.path.join(self.cwd, 'users', str(u.ID))
            self.users[u.ID].summarize(*Workspace.load_or_compute(pickle_fn, compute))

    def summarize_tags(self):
        def compute():
            movie_ratings = self.ratings.for_tag(t, movies=self.movies)
            return Workspace.summary_stats(movie_ratings)

        for t in self.movies.tags:
            pickle_fn = os.path.join(self.cwd, 'tags', str(t))
            self.tags[t] = Workspace.load_or_compute(pickle_fn, compute)

    def summarize_decades(self):
        def compute():
            movie_ratings = self.ratings.for_decade(d, movies=self.movies)
            return Workspace.summary_stats(movie_ratings)

        for d in self.movies.decades:
            pickle_fn = os.path.join(self.cwd, 'decades', str(d))
            self.decades[d] = Workspace.load_or_compute(pickle_fn, compute)

    def summarize_age_groups(self):
        def compute():
            movie_ratings = self.ratings.for_age_group(a, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for a in self.users.age_groups:
            pickle_fn = os.path.join(self.cwd, 'age_groups', str(a))
            self.age_groups[a] = Workspace.load_or_compute(pickle_fn, compute)

    def summarize_genders(self):
        def compute():
            movie_ratings = self.ratings.for_gender(g, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for g in self.users.genders:
            pickle_fn = os.path.join(self.cwd, 'genders', str(g))
            self.genders[g] = Workspace.load_or_compute(pickle_fn, compute)

    def summarize_occupations(self):
        def compute():
            movie_ratings = self.ratings.for_occupation(o, users=self.users)
            return Workspace.summary_stats(movie_ratings)

        for o in self.users.occupations:
            pickle_fn = os.path.join(self.cwd, 'occupations', str(o))
            self.occupations[o] = Workspace.load_or_compute(pickle_fn, compute)

    @staticmethod
    def load_or_compute(pickle_fn, compute):
        if os.path.isfile(pickle_fn):
            result = cPickle.load(open(pickle_fn))
        else:
            result = compute()
            cPickle.dump(result, open(pickle_fn, 'wb'))
        return result

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
