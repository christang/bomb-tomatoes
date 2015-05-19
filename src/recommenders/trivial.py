from base import BaseRecommender, Rank


class TrivialArithMeanRecommender(BaseRecommender):

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.movies[mid].amean) for mid in mid_subset]
        ratings.sort(key=lambda r: -r[1])

        last_rank = 0
        last_rating = None
        for r in ratings:
            if r[1] != last_rating:
                last_rank += 1
                last_rating = r[1]
            yield Rank(user=uid, movie=r[0], rank=last_rank, score=r[1])


class TrivialHarmMeanRecommender(BaseRecommender):

    def rank_movies(self, uid, mid_subset=None):
        mid_subset = mid_subset or self.movies.movies_by_ID.keys()
        ratings = [(mid, self.movies[mid].hmean) for mid in mid_subset]
        ratings.sort(key=lambda r: -r[1])

        last_rank = 0
        last_rating = None
        for r in ratings:
            if r[1] != last_rating:
                last_rank += 1
                last_rating = r[1]
            yield Rank(user=uid, movie=r[0], rank=last_rank, score=r[1])
