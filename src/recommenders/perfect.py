from base import BaseRecommender, Rank


class PerfectRecommender(BaseRecommender):

    def rank_movies(self, uid, mid_subset=None):
        ratings = self.ratings.for_user(uid)
        ratings = [r for r in ratings if r.m_id in mid_subset]
        ratings.sort()

        last_rank = 0
        last_rating = None
        for r in ratings:
            if r.rating != last_rating:
                last_rank += 1
                last_rating = r.rating
            yield Rank(user=r.u_id, movie=r.m_id, rank=last_rank, score=r.rating)
