import numpy as np

from churn.evaluate import best_f1_threshold, business_value, compute_metrics


def test_business_value_formula():
    y_true = np.array([1, 1, 0, 0])
    y_pred = np.array([1, 0, 1, 0])
    # 1 verdadeiro positivo e 2 abordados: 1*0.3*600 - 2*60 = 60
    assert business_value(y_true, y_pred) == 60.0


def test_best_threshold_separates_perfect_scores():
    y = np.array([0, 0, 0, 1, 1, 1])
    p = np.array([0.1, 0.2, 0.3, 0.7, 0.8, 0.9])
    thr = best_f1_threshold(y, p)
    assert 0.3 < thr <= 0.7
    assert compute_metrics(y, p, thr)["f1"] == 1.0
