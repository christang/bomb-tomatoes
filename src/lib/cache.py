import cPickle
import os


class Pickled(object):

    def __init__(self, cwd='dat/pkl'):
        self.cwd = cwd

    @staticmethod
    def load_or_compute(pickle_fn, compute):
        if os.path.isfile(pickle_fn):
            result = cPickle.load(open(pickle_fn))
        else:
            result = compute()
            cPickle.dump(result, open(pickle_fn, 'wb'))
        return result
