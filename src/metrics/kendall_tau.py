import collections
from scipy.stats import kendalltau

from base import BaseMetric


class KendallTau(collections.namedtuple('Tau', 'user tau p')):

    __slots__ = ()

    def __repr__(self):
        return 'tau(u:%d)=%4.2f[%4.2e]' % (self.user, self.tau, self.p)


class KendallTauMetric(BaseMetric):

    def evaluate(self, key):
        y_true, y_pred = self.ordered_scores(key)
        tau, p_value = kendalltau(y_true, y_pred)
        return KendallTau(user=key, tau=tau, p=p_value)
