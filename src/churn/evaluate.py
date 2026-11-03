"""Metricas tecnicas e de negocio."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

from churn.config import CUSTOMER_VALUE, RETENTION_COST, RETENTION_SUCCESS_RATE


def business_value(
    y_true,
    y_pred,
    customer_value: float = CUSTOMER_VALUE,
    retention_cost: float = RETENTION_COST,
    success_rate: float = RETENTION_SUCCESS_RATE,
) -> float:
    """Valor liquido esperado da campanha de retencao.

    Cada cliente sinalizado custa `retention_cost`. Cada churner real sinalizado
    rende `success_rate * customer_value`.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    flagged = int((y_pred == 1).sum())
    return tp * success_rate * customer_value - flagged * retention_cost


def best_f1_threshold(y_true, proba) -> float:
    """Limiar que maximiza o F1 da classe positiva."""
    precision, recall, thresholds = precision_recall_curve(y_true, proba)
    denom = precision[:-1] + recall[:-1]
    f1 = np.divide(
        2 * precision[:-1] * recall[:-1],
        denom,
        out=np.zeros_like(denom),
        where=denom > 0,
    )
    return float(thresholds[int(np.argmax(f1))])


def compute_metrics(y_true, proba, threshold: float = 0.5) -> dict[str, float]:
    """Calcula as metricas tecnicas e o valor de negocio para um limiar."""
    pred = (np.asarray(proba) >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, proba)),
        "f1": float(f1_score(y_true, pred)),
        "precision": float(precision_score(y_true, pred, zero_division=0)),
        "recall": float(recall_score(y_true, pred)),
        "business_value": float(business_value(y_true, pred)),
        "threshold": float(threshold),
    }
