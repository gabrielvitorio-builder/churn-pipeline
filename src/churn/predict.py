"""Carga do modelo salvo e predicao para um cliente."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from churn.config import FEATURES, METADATA_PATH, MODEL_PATH

HIGH_RISK_THRESHOLD = 0.70


class ModelNotAvailableError(RuntimeError):
    """O arquivo do modelo nao foi encontrado."""


@lru_cache(maxsize=1)
def load_model(path: str | Path = MODEL_PATH):
    """Carrega o pipeline treinado (cacheado em memoria)."""
    path = Path(path)
    if not path.exists():
        raise ModelNotAvailableError(
            f"Modelo nao encontrado em {path}. Rode `python -m churn.train` para gerar."
        )
    return joblib.load(path)


@lru_cache(maxsize=1)
def load_metadata(path: str | Path = METADATA_PATH) -> dict[str, Any]:
    """Le os metadados do modelo (limiar, metricas, versao)."""
    path = Path(path)
    if not path.exists():
        raise ModelNotAvailableError(f"Metadados nao encontrados em {path}.")
    return json.loads(path.read_text(encoding="utf-8"))


def risk_level(probability: float, threshold: float) -> str:
    """Traduz a probabilidade em nivel de risco para o time de retencao."""
    if probability >= HIGH_RISK_THRESHOLD:
        return "alto"
    if probability >= threshold:
        return "medio"
    return "baixo"


def to_dataframe(records: list[dict[str, Any]]) -> pd.DataFrame:
    """Monta o DataFrame de entrada na ordem e nos tipos esperados pelo pipeline."""
    df = pd.DataFrame(records)
    missing = [c for c in FEATURES if c not in df.columns]
    for col in missing:
        df[col] = np.nan
    df = df[FEATURES].copy()
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(str)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def predict_customer(record: dict[str, Any]) -> dict[str, Any]:
    """Retorna probabilidade, classe e nivel de risco de churn para um cliente."""
    model = load_model()
    threshold = float(load_metadata()["threshold"])
    proba = float(model.predict_proba(to_dataframe([record]))[0, 1])
    return {
        "churn_probability": round(proba, 4),
        "churn_prediction": bool(proba >= threshold),
        "risk_level": risk_level(proba, threshold),
        "threshold": round(threshold, 4),
    }
