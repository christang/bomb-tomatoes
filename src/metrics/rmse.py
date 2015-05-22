import collections
import math
from sklearn.metrics import mean_squared_error

from base import BaseMetric


class RMSEFold(collections.namedtuple('RMSE', 'fold rmse')):

    __slots__ = ()

    def __repr__(self):
        return 'rmse(f:%s)=%4.2f' % (str(self.fold), self.rmse)


class RMSEUser(collections.namedtuple('RMSE', 'user rmse')):

    __slots__ = ()

    def __repr__(self):
        return 'rmse(u:%s)=%4.2f' % (str(self.user), self.rmse)


class RMSEMetric(BaseMetric):

    def evaluate(self, key):
        y_true, y_pred = self.ordered_scores(key)
        rmse = math.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))
        return RMSEUser(user=key, rmse=rmse)

    def evaluate_all(self):
        all_true = []
        all_pred = []
        for key in self.keys():
            y_true, y_pred = self.ordered_scores(key)
            all_true.extend(y_true)
            all_pred.extend(y_pred)
        rmse = math.sqrt(mean_squared_error(y_true=all_true, y_pred=all_pred))
        return [RMSEFold(fold=self.label, rmse=rmse)]
