import cPickle
import numpy as np
from sklearn import decomposition
import os

from lib.folds import SimpleUserFolds
from lib.workspace import load_data


def save_components(cwd, A, split, movies_map):
    def compute():
        return A[movies_map[m_id], :]

    for m_id, i in movies_map.items():
        pickle_fn = os.path.join(cwd, 'components', '%02d' % split, str(m_id))
        load_or_compute(pickle_fn, compute)


def load_or_compute(pickle_fn, compute):
    if os.path.isfile(pickle_fn):
        result = cPickle.load(open(pickle_fn))
    else:
        result = compute()
        cPickle.dump(result, open(pickle_fn, 'wb'))
    return result


def build_features_matrix(k, movies, ratings):
    tags = sorted(movies.tags)
    decades = sorted(movies.decades)
    rated_movies = {m_id: i for i, m_id in enumerate([m.ID for m in movies.movies if m.count > 0])}
    training_set_users = {u_id: i for i, u_id in enumerate(SimpleUserFolds.training_set(k))}
    shape = (len(rated_movies), len(training_set_users) + len(tags) + len(decades))

    # We take zero to be the center of the distribution.
    # when there is no data, the user is taken to have no preference liking or disliking the movie
    A = np.zeros(shape)
    for rating in ratings.ratings:
        if rating.u_id in training_set_users:
            A[rated_movies[rating.m_id], training_set_users[rating.u_id]] = \
                rating.rating - movies[rating.m_id].amean

    for m_id, i in rated_movies.items():
        for j, tag in enumerate(tags):
            s = 1 if tag in movies[m_id].tags else 0
            A[i, len(training_set_users) + j] = s

    for m_id, i in rated_movies.items():
        for j, decade in enumerate(decades):
            s = 1 if decade == movies[m_id].decade() else 0
            A[i, len(training_set_users) + len(tags) + j] = s

    return A, rated_movies


def main():
    cwd = 'dat/ml-1m'
    workspace = load_data(cwd)
    print "Loaded: Users, Movies, Ratings"

    for split in xrange(1, 2):
        A, movies_map = build_features_matrix(split, workspace.movies, workspace.ratings)
        pca = decomposition.RandomizedPCA(n_components=100)
        pca.fit(A)
        print pca.explained_variance_ratio_
        print "Ratio of explained variances: %f" % (sum(pca.explained_variance_ratio_))
        save_components('dat/pkl', pca.transform(A), split, movies_map)

if __name__ == '__main__':
    main()
