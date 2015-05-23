from collections import defaultdict
import numpy as np

from base import BaseRecommender


class UserProfile(object):

    untagged = 0.001

    def __init__(self, user, movies, ratings):
        self.user = user
        self.ratings = ratings
        self.f_coeffs = UserProfile.build_coeffs(ratings, movies)
        #print 'f_coeffs = ', self.f_coeffs

    def rate(self, movie):
        score = movie.hmean
        for tag, coeff in self.f_coeffs.items():
            a = 1 if tag in movie.tags else UserProfile.untagged
            score += a * coeff
        return score

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
                A[i, j] = 1 if tag in movies[m_id].tags else UserProfile.untagged
            b[i, 0] = ratings[m_id] - movies[m_id].hmean

        if len(m_index) < 1000:
            x = UserProfile.solve_least_squares(A, b)
        else:
            # don't solve for now
            raise Exception('too many movies')
        return {f: x[i, 0] for i, f in enumerate(f_index)}

    @staticmethod
    def solve_normal_equations(A, b):
        # We seek to minimize: L2||Ax-b||
        # => (A'A)^-1 dot A' dot b
        # => pinv(A) dot b
        x = np.linalg.pinv(A).dot(b)
        return x

    @staticmethod
    def solve_least_squares(A, b):
        x, resid, rank, s = np.linalg.lstsq(A, b, rcond=UserProfile.untagged)
        return x


class BomTomRecommender(BaseRecommender):

    def __init__(self, users, movies, ratings):
        super(BomTomRecommender, self).__init__(users, movies, ratings)
        self.profiles = {}

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.profiles[uid].rate(self.movies[mid])) for mid in mid_subset]
        for rank in BaseRecommender.sort_and_yield(ratings, uid):
            yield rank

    def train(self, training_set_gen):
        r_ids = list(training_set_gen)

        users = defaultdict(dict)
        for r_id in r_ids:
            r = self.ratings.ratings[r_id]
            users[r.u_id][r.m_id] = r.rating

        for u_id, ratings in users.items():
            self.profiles[u_id] = UserProfile(self.users[u_id], self.movies, ratings)
