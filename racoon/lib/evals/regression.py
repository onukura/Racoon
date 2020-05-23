# -*- coding: utf-8 -*-
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error


class MetricRegression:
    @staticmethod
    def score_mae(yhat, y):
        return mean_absolute_error(yhat, y)

    @staticmethod
    def score_mse(yhat, y):
        return mean_squared_error(yhat, y)

    @staticmethod
    def score_msle(yhat, y):
        return mean_squared_log_error(yhat, y)

    @staticmethod
    def score_rmse(yhat, y):
        return np.sqrt(MetricRegression.score_mse(yhat, y))

    @staticmethod
    def list_metric():
        methods_all = dir(MetricRegression)
        methods = []
        [methods.append(method) for method in methods_all if "score_" in method]
        return methods
