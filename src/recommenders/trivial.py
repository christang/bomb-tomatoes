from base import BaseRecommender


class TrivialArithMeanRecommender(BaseRecommender):

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.movies[mid].amean) for mid in mid_subset]
        for rank in BaseRecommender.sort_and_yield(ratings, uid):
            yield rank


class TrivialHarmMeanRecommender(BaseRecommender):

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.movies[mid].hmean) for mid in mid_subset]
        for rank in BaseRecommender.sort_and_yield(ratings, uid):
            yield rank
