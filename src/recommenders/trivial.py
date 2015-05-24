from base import BaseRecommender


class TrivialArithMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return round(movie.amean)


class TrivialHarmMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return round(movie.hmean)