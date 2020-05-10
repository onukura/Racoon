import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error


def mae(yhat, y):
    return mean_absolute_error(yhat, y)


def mse(yhat, y):
    return mean_squared_error(yhat, y)


def msle(yhat, y):
    return mean_squared_log_error(yhat, y)


def rmse(yhat, y):
    return np.sqrt(mse(yhat, y))
