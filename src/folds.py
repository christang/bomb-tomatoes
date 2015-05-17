from workspace import *

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


def expand(kf):
    return [(train, test) for train, test in kf]


if __name__ == '__main__':
    w = get_workspace('dat/ml-1m')
    f = Folds(w.users, 5)
    f.show(5)
