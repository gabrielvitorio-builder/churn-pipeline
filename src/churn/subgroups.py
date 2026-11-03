"""Metricas por subgrupo (genero e idoso) para a analise de vieses do Model Card.

Uso:
    python -m churn.subgroups
"""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import precision_score, recall_score

from churn.config import RESULTS_DIR
from churn.data import clean_data, load_raw_data, make_train_test
from churn.predict import load_metadata, load_model


def subgroup_metrics(group_cols=("gender", "SeniorCitizen")) -> pd.DataFrame:
    """Taxa de churn real, taxa de sinalizacao, precisao e recall por subgrupo (teste)."""
    df = clean_data(load_raw_data())
    _, X_test, _, y_test = make_train_test(df)
    thr = float(load_metadata()["threshold"])
    pred = (load_model().predict_proba(X_test)[:, 1] >= thr).astype(int)

    rows = []
    for col in group_cols:
        for value in sorted(X_test[col].unique()):
            mask = (X_test[col] == value).to_numpy()
            rows.append(
                {
                    "atributo": col,
                    "grupo": value,
                    "clientes": int(mask.sum()),
                    "churn_real": round(float(y_test[mask].mean()), 4),
                    "taxa_sinalizados": round(float(pred[mask].mean()), 4),
                    "precisao": round(float(precision_score(y_test[mask], pred[mask])), 4),
                    "recall": round(float(recall_score(y_test[mask], pred[mask])), 4),
                }
            )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = subgroup_metrics()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(RESULTS_DIR / "subgroup_metrics.csv", index=False)
    print(table.to_string(index=False))
