import random

from sklearn import cross_validation


class Folds(object):

    def __init__(self, users, k=5, limit_users=6040):
        self.k = k
        self.users = users
        self.folds = {u.ID: expand(cross_validation.KFold(u.count, n_folds=k, shuffle=True))
                      for u in users.users if u.ID <= limit_users}

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
