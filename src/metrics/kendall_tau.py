import collections
import logging
from scipy.stats import kendalltau

from base import BaseMetric


class KendallTauFold(collections.namedtuple('Tau', 'fold tau p')):

    __slots__ = ()

    def __repr__(self):
        return 'tau(f:%s)=%4.2f[%4.2e]' % (str(self.fold), self.tau, self.p)


class KendallTauUser(collections.namedtuple('Tau', 'user tau p')):

    __slots__ = ()

    def __repr__(self):
        return 'tau(u:%s)=%4.2f[%4.2e]' % (str(self.user), self.tau, self.p)


class KendallTauMetric(BaseMetric):

    def evaluate(self, key):
        y_true, y_pred = self.ordered_scores(key)
        tau, p_value = kendalltau(y_true, y_pred)
        return KendallTauUser(user=key, tau=tau, p=p_value)

    def evaluate_all(self):
        all_true = []
        all_pred = []
        logging.info((self.name, self.fold))
        for key in self.keys():
            y_true, y_pred = self.ordered_scores(key)
            if self.debug:
                tau, p_value = kendalltau(y_true, y_pred)
                logging.info(KendallTauUser(user=key, tau=tau, p=p_value))
            all_true.extend(y_true)
            all_pred.extend(y_pred)
        tau, p_value = kendalltau(all_true, all_pred)
        stat = KendallTauFold(fold=self.fold, tau=tau, p=p_value)
        logging.info(stat)
        return [stat]
