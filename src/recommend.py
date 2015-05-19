import os

from folds import Folds
from metrics.rmse import RMSEMetric
from metrics.kendall_tau import KendallTauMetric
from models.movies import Movies
from models.ratings import Ratings
from models.users import Users
from recommenders.base import Rank
from recommenders.perfect import PerfectRecommender
from recommenders.trivial import TrivialArithMeanRecommender, TrivialHarmMeanRecommender
from workspace import Workspace


def get_guess(recommender, truth, uid):
    def _generator():
        return recommender.rank_users_movies([uid], [m.movie for m in truth[uid]])[uid]
    return [r for r in _generator()]


def get_truth(uid, ratings, k, folds):
    def _generator():
        last_rank = 0
        last_rating = None
        for sr in sorted_ratings:
            if sr.rating != last_rating:
                last_rank += 1
                last_rating = sr.rating
            yield Rank(user=sr.u_id, movie=sr.m_id, rank=last_rank, score=sr.rating)
    sorted_ratings = sorted(ratings.get(folds.test_on(k, [uid])))
    return [r for r in _generator()]


def get_performance(users, movies, ratings, k, uid_subset, metrics, Recommender):
    folds = Folds(users)
    recommender = Recommender(users, movies, ratings)
    recommender.train(folds.train_on(k, uid_subset))
    truth = {}
    guess = {}

    for uid in uid_subset:
        truth[uid] = get_truth(uid, ratings, k, folds)
        guess[uid] = get_guess(recommender, truth, uid)

    return (m(truth, guess) for m in metrics)


def load_data(data_dir):
    users = Users.parse_stream(open(os.path.join(data_dir, 'users.dat')))
    movies = Movies.parse_stream(open(os.path.join(data_dir, 'movies.dat')))
    ratings = Ratings.parse_stream(open(os.path.join(data_dir, 'ratings.dat')))

    w = Workspace(movies, ratings, users)
    w.summarize_users()
    w.summarize_movies()
    return users, movies, ratings


def main():
    cwd = 'dat/ml-1m'
    users, movies, ratings = load_data(cwd)

    uid_subset = [1, 6040]
    metrics = (RMSEMetric, KendallTauMetric)
    recommenders = (PerfectRecommender, TrivialArithMeanRecommender, TrivialHarmMeanRecommender)

    for recommender in recommenders:
        print recommender.__name__
        for k in xrange(2):
            perf = get_performance(users, movies, ratings, k, uid_subset, metrics, recommender)
            print 'Fold %d' % (k+1)
            print '======'
            for p in perf:
                print p

        print


if __name__ == '__main__':
    main()
