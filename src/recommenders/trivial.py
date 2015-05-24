from base import BaseRecommender


class TrivialArithMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return movie.amean


class TrivialHarmMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return movie.hmean