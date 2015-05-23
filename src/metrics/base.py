

class BaseMetric(object):

    def __init__(self, truth, guess, name='?', fold='?', debug=True):
        self.truth = truth
        self.guess = guess
        self.name = name
        self.fold = fold
        self.debug = debug

    def evaluate(self, key):
        return None

    def evaluate_all(self):
        return [self.evaluate(key) for key in self.keys()]

    def evaluate_summary(self):
        return ' '.join([str(e) for e in self.evaluate_all()])

    def keys(self):
        return self.truth.keys()

    def ordered_scores(self, key):
        y_actual = [r.score for r in sorted(self.truth[key], key=lambda _: _.movie)]
        y_predict = [r.score for r in sorted(self.guess[key], key=lambda _: _.movie)]
        return y_actual, y_predict

    def __repr__(self):
        return '%s : %s' % (self.__class__.__name__, self.evaluate_summary())
