# -*- coding: utf-8 -*-
from racoon.lib.evals.regression import MetricRegression
from racoon.lib.evals.classifier import MetricClassification


metrics = {
    "regression": MetricRegression,
    "classification": MetricClassification,
}
