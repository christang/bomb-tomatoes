import numpy as np
from sklearn import cluster

from lib.workspace import load_data


def get_features(users, movies):
    shape = (len(users), len(movies))
    features = np.zeros(shape)

    # stub

    return features


def get_connectivity(users, cutoff=250):
    shape = (len(users), len(users))
    connectivity = np.zeros(shape)
    for i, u1 in enumerate(users):
        for j, u2 in enumerate(users):
            connectivity[i,j] = 1 if u1.zip_code.miles_to(u2.zip_code) < cutoff else 0
    return connectivity


def main():
    n_cluster = 25
    cwd = 'dat/ml-1m'
    workspace = load_data(cwd)
    connectivity = get_connectivity(workspace.users.users)
    features = get_features(workspace.users.users, workspace.movies.movies)

    agc = cluster.AgglomerativeClustering(n_cluster, connectivity, linkage='ward')
    agc.fit(features)

    # ....


if __name__ == '__main__':
    main()
