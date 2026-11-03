"""Definicao dos modelos candidatos (linear, arvores e rede neural)."""

from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

from churn.config import SEED
from churn.preprocessing import build_preprocessor


def get_models(seed: int = SEED) -> dict[str, Pipeline]:
    """Retorna os tres candidatos, cada um com o mesmo pre-processamento."""
    return {
        "logistic_regression": Pipeline(
            [
                ("prep", build_preprocessor()),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=1000, class_weight="balanced", random_state=seed
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("prep", build_preprocessor()),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=10,
                        min_samples_leaf=5,
                        class_weight="balanced_subsample",
                        n_jobs=-1,
                        random_state=seed,
                    ),
                ),
            ]
        ),
        "mlp": Pipeline(
            [
                ("prep", build_preprocessor()),
                (
                    "clf",
                    MLPClassifier(
                        hidden_layer_sizes=(64, 32),
                        alpha=1e-3,
                        early_stopping=True,
                        validation_fraction=0.1,
                        n_iter_no_change=10,
                        max_iter=500,
                        random_state=seed,
                    ),
                ),
            ]
        ),
    }
