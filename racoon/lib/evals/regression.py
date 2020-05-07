import numpy as np


def mae(yhat, y):
    return float(np.mean(np.abs(yhat - y)))


def mse(yhat, y):
    return float(np.mean((yhat - y) ** 2))


def rmse(yhat, y):
    return float(np.std(yhat - y))
