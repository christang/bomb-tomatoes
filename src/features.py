import cPickle
import numpy as np
from sklearn import decomposition
import os

from lib.io import load_data
from lib.folds import SimpleUserFolds


def save_components(cwd, A, k, movies_map):
    def compute():
        return A[movies_map[m_id], :]

    components = {}
    for m_id, i in movies_map.items():
        pickle_fn = os.path.join(cwd, 'components', '%02d' % k, str(m_id))
        components[m_id] = load_or_compute(pickle_fn, compute)

    return components


def load_or_compute(pickle_fn, compute):
    if os.path.isfile(pickle_fn):
        result = cPickle.load(open(pickle_fn))
    else:
        result = compute()
        cPickle.dump(result, open(pickle_fn, 'wb'))
    return result


def build_features_matrix(k, movies, ratings):
    tags = sorted(movies.tags)
    rated_movies = {m_id: i for i, m_id in enumerate([m.ID for m in movies.movies if m.count > 0])}
    training_set_users = {}
    shape = (len(rated_movies), len(training_set_users) + len(tags))

    A = np.zeros(shape)
    for rating in ratings.ratings:
        if rating.u_id in training_set_users:
            A[rated_movies[rating.m_id], training_set_users[rating.u_id]] = \
                rating.rating - movies[rating.m_id].amean

    for m_id, i in rated_movies.items():
        for j, tag in enumerate(tags):
            s = 1 if tag in movies[m_id].tags else 0.0001
            A[i, len(training_set_users) + j] = s

    return A, rated_movies


def main():
    cwd = 'dat/ml-1m'
    users, movies, ratings = load_data(cwd, False)
    print "Loaded: Users, Movies, Ratings"

    for k in xrange(1, 2):
        A, movies_map = build_features_matrix(k, movies, ratings)
        pca = decomposition.PCA(n_components=6)
        pca.fit(A)
        print pca.explained_variance_ratio_
        print "Ratio of explained variances: %f" % (sum(pca.explained_variance_ratio_))
        save_components('dat/pkl', pca.transform(A), k, movies_map)

if __name__ == '__main__':
    main()
