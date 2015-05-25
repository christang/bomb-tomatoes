import numpy as np
from scipy import sparse
from sklearn import feature_selection

from lib.folds import SimpleUserFolds
from lib.workspace import load_data, Workspace
from models.ratings import Ratings


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

    return A, b1, b2, b3, training_set_users, rated_movies


def recover_gender_gap(u_ids, m_ids, workspace):
    biases = []
    for m_id in m_ids:
        ratings = Ratings(workspace.ratings.for_subset(u_ids, [m_id]))
        biases.append({
            'f': Workspace.summary_stats(ratings.for_gender(False, workspace.users)),
            'm': Workspace.summary_stats(ratings.for_gender(True, workspace.users))
        })
    return biases


def recover_generation_gap(u_ids, m_ids, workspace):
    return []


def recover_occupation_gap(u_ids, m_ids, workspace):
    return []


def main():
    cwd = 'dat/ml-1m'
    workspace = load_data(cwd)
    print "Loaded: Users, Movies, Ratings"

    split = 1

    A, b1, b2, b3, users_map, movies_map = \
        build_features_matrix(split, workspace.users, workspace.movies, workspace.ratings)
    chi2 = feature_selection.SelectKBest(feature_selection.chi2)
    inv_movies_map = {i: m_id for m_id, i in movies_map.items()}

    print '\nby gender'
    chi2.fit(A, b1)
    supports = chi2.get_support(True)
    selected = [(chi2.pvalues_[i], workspace.movies[inv_movies_map[i]]) for i in supports]
    selected.sort(key=lambda s: s[0])
    stats = recover_gender_gap(users_map.keys(), [m.ID for _, m in selected], workspace)
    for s1, s2 in zip(selected, stats):
        n = s2['m'][1] + s2['f'][1]
        r = float(s2['m'][1]) / float(s2['f'][1])
        l = 'male-to-female' if r >= 1 else 'female-to-male'
        r = 1.0 / r if r < 1 else r
        print 'n=%4s mean(M)=%4.2f mean(F)=%4.2f %s=%4.2f %s' % \
              (n, s2['m'][2], s2['f'][2], l, r, s1[1])

if __name__ == '__main__':
    main()
