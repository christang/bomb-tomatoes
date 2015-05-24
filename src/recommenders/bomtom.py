from collections import defaultdict
import numpy as np

from base import BaseRecommender


class UserProfile(object):

    tolerance = 0.001

    def __init__(self, user, ratings):
        self.user = user
        self.ratings = ratings

    def predict(self, movie):
        return 0

    @staticmethod
    def solve_normal_equations(A, b):
        """
        We seek to minimize: L2||Ax-b||
         => (A'A)^-1 dot A' dot b
         => pinv(A) dot b

        :param A: matrix of movie features having shape (# movies, # features)
        :param b: vector of user's ratings preferences
        :return: vector of coefficients minimizing L2 ||Ax-b||
        """
        x = np.linalg.pinv(A).dot(b)
        return x

    @staticmethod
    def solve_least_squares(A, b):
        x, resid, rank, s = np.linalg.lstsq(A, b, rcond=UserProfile.tolerance)
        return x


class TagBasedProfile(UserProfile):

    def __init__(self, user, movies, ratings):
        super(TagBasedProfile, self).__init__(user, ratings)
        self.f_coeffs = TagBasedProfile.build_coeffs(ratings, movies)

    def predict(self, movie):
        score = movie.amean
        for tag, coeff in self.f_coeffs.items():
            a = 1 if tag in movie.tags else UserProfile.tolerance
            score += a * coeff
        return min(5, max(1, round(score)))

    @staticmethod
    def build_coeffs(ratings, movies):
        m_index = sorted(ratings.keys())
        f_index = sorted(set(t for m_id in m_index for t in movies[m_id].tags))
        A_shape = (len(m_index), len(f_index))
        A = np.zeros(A_shape)
        b_shape = (len(m_index), 1)
        b = np.zeros(b_shape)

        for i, m_id in enumerate(m_index):
            for j, tag in enumerate(f_index):
                # Take MovieLens tags at *mostly* face value :-)
                A[i, j] = 1 if tag in movies[m_id].tags else UserProfile.tolerance
            b[i, 0] = ratings[m_id] - movies[m_id].amean

        if len(m_index) < 1000:
            x = UserProfile.solve_least_squares(A, b)
        else:
            # don't solve for now
            raise Exception('too many movies')
        return {f: x[i, 0] for i, f in enumerate(f_index)}


class ComponentBasedProfile(UserProfile):

    def __init__(self, user, movies, ratings):
        super(ComponentBasedProfile, self).__init__(user, ratings)
        self.f_coeffs = ComponentBasedProfile.build_coeffs(ratings, movies)

    def predict(self, movie):
        score = movie.components.dot(self.f_coeffs) + movie.amean
        return min(5, max(1, round(score)))

    @staticmethod
    def build_coeffs(ratings, movies):
        m_index = sorted(ratings.keys())
        n_comps = len(movies.movies[0].components)
        A_shape = (len(m_index), n_comps)
        A = np.zeros(A_shape)
        b_shape = (len(m_index), 1)
        b = np.zeros(b_shape)

        for i, m_id in enumerate(m_index):
            A[i, :] = movies[m_id].components
            b[i, 0] = ratings[m_id] - movies[m_id].amean

        if len(m_index) < 1000:
            x = UserProfile.solve_least_squares(A, b)
        else:
            # don't solve for now
            raise Exception('too many movies')
        return x[:, 0]


class BomTomRecommender(BaseRecommender):

    def __init__(self, users, movies, ratings):
        super(BomTomRecommender, self).__init__(users, movies, ratings)
        self.profiles = {}

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.profiles[uid].predict(self.movies[mid])) for mid in mid_subset]
        for rank in BaseRecommender.sort_and_yield(ratings, uid):
            yield rank

    def train(self, training_set_gen):
        r_ids = list(training_set_gen)

        users = defaultdict(dict)
        for r_id in r_ids:
            r = self.ratings.ratings[r_id]
            users[r.u_id][r.m_id] = r.rating

        for u_id, ratings in users.items():
            self.profiles[u_id] = ComponentBasedProfile(self.users[u_id], self.movies, ratings)
