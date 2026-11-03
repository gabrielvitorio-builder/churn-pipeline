"""Carga, limpeza e divisao dos dados."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from churn.config import (
    FEATURES,
    ID_COLUMN,
    RAW_DATA_PATH,
    SEED,
    TARGET,
    TEST_SIZE,
)


def load_raw_data(path: Path | str = RAW_DATA_PATH) -> pd.DataFrame:
    """Le o CSV bruto do Telco Customer Churn."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica a limpeza basica ao dataset.

    - TotalCharges vem como texto e tem espacos em branco para clientes com
      tenure 0. Convertemos para numerico e deixamos NaN (imputado depois, no
      pipeline, para evitar vazamento de dados).
    - SeniorCitizen e tratado como categoria ("0"/"1").
    - Churn vira 0/1 quando presente.
    """
    out = df.copy()
    out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")
    out["SeniorCitizen"] = out["SeniorCitizen"].astype(str)
    if TARGET in out.columns:
        out[TARGET] = out[TARGET].map({"Yes": 1, "No": 0}).astype(int)
    if ID_COLUMN in out.columns:
        out = out.drop(columns=[ID_COLUMN])
    return out


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separa X (features do modelo) e y (alvo)."""
    return df[FEATURES], df[TARGET]


def make_train_test(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    seed: int = SEED,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide em treino e teste de forma estratificada e reprodutivel."""
    X, y = split_features_target(df)
    return train_test_split(X, y, test_size=test_size, stratify=y, random_state=seed)
