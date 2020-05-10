# -*- coding: utf-8 -*-
from unittest import TestCase
import numpy as np

from racoon.lib.evals.regression import mae, mse, msle, rmse


class Test(TestCase):
    def setUp(self) -> None:
        self.answer = np.array([1, 2, 3, 4, 5])
        self.predict = np.array([2, 2, 2, 2, 2])

    def test_mae(self):
        r = float(np.abs((self.answer - self.predict)).mean())
        self.assertEqual(r, mae(self.answer, self.predict))

    def test_mse(self):
        r = float(np.mean((self.answer - self.predict) ** 2))
        self.assertEqual(r, mse(self.answer, self.predict))

    def test_msle(self):
        r = float(np.mean((np.log1p(self.answer) - np.log1p(self.predict)) ** 2))
        self.assertEqual(r, msle(self.answer, self.predict))

    def test_rmse(self):
        r = float(np.sqrt(np.mean((self.answer - self.predict) ** 2)))
        self.assertEqual(r, rmse(self.answer, self.predict))
