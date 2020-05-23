# -*- coding: utf-8 -*-
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import auc


class MetricClassification:
    @staticmethod
    def score_accuracy(yhat, y):
        return accuracy_score(yhat, y)

    @staticmethod
    def score_f1(yhat, y):
        return f1_score(yhat, y)

    @staticmethod
    def score_auc(yhat, y):
        return auc(yhat, y)
