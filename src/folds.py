from workspace import *

import random
from sklearn import cross_validation


class Folds(object):

    def __init__(self, users, k=5, limit_users=6040):
        self.k = k
        self.users = users
        self.folds = {u.ID: expand(cross_validation.KFold(u.count, n_folds=k, shuffle=True))
                      for u in users.users if u.ID <= limit_users}

    def show(self, first_n=25):
        train = []
        test = []

        for k in xrange(self.k):
            train.append([])
            test.append([])

        for u_id, kf in self.folds.items():
            k = 0
            for train_index, test_index in kf:
                train[k].extend([str(self.users[u_id].r_ids[i]) for i in train_index])
                test[k].extend([str(self.users[u_id].r_ids[i]) for i in test_index])
                k += 1

        for k in xrange(self.k):
            print "TRAIN %d %s" % (k, ','.join(train[k][:first_n]))
            print "TEST %d %s" % (k, ','.join(test[k][:first_n]))

    def train_on(self, k, uid_subset=None):
        uid_subset = uid_subset or self.folds.keys()
        for rid in Folds.shuffle_rids(uid_subset, k, self.folds, self.users, 0):
            yield rid

    def test_on(self, k, uid_subset=None):
        uid_subset = uid_subset or self.folds.keys()
        for rid in Folds.shuffle_rids(uid_subset, k, self.folds, self.users, 1):
            yield rid

    @staticmethod
    def shuffle_rids(uid_subset, k, folds, users, train_or_test):
        rids = []
        for uid in uid_subset:
            user_rids = [users[uid].r_ids[rid] for rid in folds[uid][k][train_or_test]]
            rids.extend(user_rids)
        random.shuffle(rids)
        return rids


def expand(kf):
    return [(train, test) for train, test in kf]


if __name__ == '__main__':
    w = get_workspace('dat/ml-1m')
    f = Folds(w.users, 5)
    f.show(5)
