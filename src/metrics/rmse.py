import collections
import math
from sklearn.metrics import mean_squared_error

from base import BaseMetric


class RMSE(collections.namedtuple('RMSE', 'user rmse')):

    __slots__ = ()

    def __repr__(self):
        return 'rmse(u:%d)=%4.2f' % (self.user, self.rmse)


class RMSEMetric(BaseMetric):

    def evaluate(self, key):
        y_true, y_pred = self.ordered_scores(key)
        rmse = math.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))
        return RMSE(user=key, rmse=rmse)
