import collections


Rank = collections.namedtuple('Rank', 'user movie rank score')


class BaseRecommender(object):

    default_score = 3.5

    def __init__(self, users, movies, ratings):
        self.users = users
        self.movies = movies
        self.ratings = ratings

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        for mid in mid_subset:
            yield Rank(user=uid, movie=mid, rank=1, score=BaseRecommender.default_score)

    def rank_users_movies(self, uid_subset=None, mid_subset=None):
        uid_subset = uid_subset or xrange(1, len(self.users.users) + 1)
        return {uid: self.rank_movies(uid, mid_subset) for uid in uid_subset}

    @staticmethod
    def sort_and_yield(ratings, uid):
        ratings.sort(key=lambda r: -r[1])

        last_rank = 0
        last_rating = None
        for r in ratings:
            if r[1] != last_rating:
                last_rank += 1
                last_rating = r[1]
            yield Rank(user=uid, movie=r[0], rank=last_rank, score=r[1])

    def train(self, training_set_gen):
        pass

    def test(self, test_set_gen):
        pass
