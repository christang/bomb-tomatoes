import random

from base import BaseRecommender


class TrivialArithMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return round(movie.amean)


class TrivialHarmMeanRecommender(BaseRecommender):

    def predict(self, movie):
        return round(movie.hmean)


class RandomRecommender(BaseRecommender):

    def predict(self, movie):
        return random.choice([1, 2, 3, 4, 5])
