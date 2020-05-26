# -*- coding: utf-8 -*-
import pandas as pd

from racoon.lib.evals.regression import MetricRegression
from racoon.lib.evals.classifier import MetricClassification


class Metric:

    metrics = {
        "regression": MetricRegression,
        "classification": MetricClassification,
    }

    def __init__(
        self,
        answer: pd.DataFrame,
        prediction: pd.DataFrame,
        metric_type: str,
        metric_name: str,
    ):
        self.answer = answer
        self.prediction = prediction
        self.func = getattr(self.metrics.get(metric_type), metric_name)

    def check_prediction(self):
        assert self.prediction.shape == self.answer.shape  # shape check
        # assert (
        #     self.prediction.iloc[:, 0].dtype == self.answer.iloc[:, 0].dtype
        # )  # type check
        # assert (
        #     self.prediction.iloc[:, 1].dtype == self.answer.iloc[:, 1].dtype
        # )  # type check
        assert (
            sum(self.answer.iloc[:, 0] == self.prediction.iloc[:, 0])
            == self.answer.shape[0]
        )  # key check

    def preprocess(self):
        return pd.merge(self.answer, self.prediction, on="id", how="inner")

    def calc_score(self) -> float:
        df = self.preprocess()
        df.dropna(inplace=True)
        return self.func(df["y"], df["yhat"])
