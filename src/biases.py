import numpy as np
from scipy import sparse
from sklearn import feature_selection

from lib.folds import SimpleUserFolds
from lib.workspace import load_data


def build_features_matrix(k, users, movies, ratings):
    rated_movies = {m_id: i for i, m_id in enumerate([m.ID for m in movies.movies if m.count > 20])}
    training_set_users = {u_id: i for i, u_id in enumerate(SimpleUserFolds.training_set(k))}
    shape = (len(training_set_users), len(rated_movies))
    b_shape = (len(training_set_users),)

    A = sparse.dok_matrix(shape)
    for rating in ratings.ratings:
        if rating.u_id in training_set_users and rating.m_id in rated_movies:
            A[training_set_users[rating.u_id], rated_movies[rating.m_id]] = rating.rating

    b1 = np.zeros(b_shape)  # M/F
    b2 = np.zeros(b_shape)  # age group
    b3 = np.zeros(b_shape)  # occupation
    for u_id, i in training_set_users.items():
        b1[i] = users[u_id].is_male
        b2[i] = users[u_id].age_group
        b3[i] = users[u_id].occupation

    return A, b1, b2, b3, rated_movies


def main():
    cwd = 'dat/ml-1m'
    workspace = load_data(cwd)
    print "Loaded: Users, Movies, Ratings"

    split = 1

    A, b1, b2, b3, movies_map = build_features_matrix(split, workspace.users, workspace.movies, workspace.ratings)
    chi2 = feature_selection.SelectKBest(feature_selection.chi2)
    inv_movies_map = {i: m_id for m_id, i in movies_map.items()}

    for b, label in zip((b1, b2, b3), ('gender', 'age group', 'occupation')):
        print '\nby %s' % label
        chi2.fit(A, b)
        selected = [(chi2.pvalues_[i], workspace.movies[inv_movies_map[i]])
                    for i in chi2.get_support(True)]
        selected.sort(key=lambda s: s[0])
        print '\n'.join([str(s) for s in selected])

if __name__ == '__main__':
    main()
