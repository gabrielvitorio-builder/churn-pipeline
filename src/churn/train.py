"""Treino, comparacao dos modelos e persistencia do campeao.

Uso:
    python -m churn.train
"""

from __future__ import annotations

import json
from datetime import date

import joblib
import pandas as pd
import sklearn
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate

from churn.config import (
    CV_FOLDS,
    FEATURES,
    METADATA_PATH,
    MODEL_PATH,
    MODELS_DIR,
    RESULTS_DIR,
    SEED,
)
from churn.data import clean_data, load_raw_data, make_train_test
from churn.evaluate import best_f1_threshold, compute_metrics
from churn.models import get_models

SCORING = {"roc_auc": "roc_auc", "f1": "f1", "precision": "precision", "recall": "recall"}


def compare_models(X_train, y_train, X_test, y_test) -> tuple[pd.DataFrame, dict]:
    """Valida cada modelo com CV no treino e mede o desempenho no teste.

    O limiar de decisao de cada modelo e escolhido com previsoes out-of-fold do
    treino (maximizando o F1), sem tocar no conjunto de teste.
    """
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=SEED)
    rows, fitted, thresholds = [], {}, {}

    for name, pipe in get_models().items():
        cv_res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=SCORING, n_jobs=1)
        oof = cross_val_predict(pipe, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
        thr = best_f1_threshold(y_train, oof)

        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]
        test = compute_metrics(y_test, proba, thr)

        row = {"model": name, "threshold": round(thr, 4)}
        for metric in SCORING:
            scores = cv_res[f"test_{metric}"]
            row[f"cv_{metric}_mean"] = round(float(scores.mean()), 4)
            row[f"cv_{metric}_std"] = round(float(scores.std()), 4)
        for metric in ("roc_auc", "f1", "precision", "recall", "business_value"):
            row[f"test_{metric}"] = round(test[metric], 4)
        rows.append(row)
        fitted[name] = pipe
        thresholds[name] = thr
        print(f"{name:22s} cv_auc={row['cv_roc_auc_mean']:.4f} test_auc={row['test_roc_auc']:.4f}")

    table = pd.DataFrame(rows).sort_values("cv_roc_auc_mean", ascending=False)
    return table, {"models": fitted, "thresholds": thresholds}


def main() -> None:
    df = clean_data(load_raw_data())
    X_train, X_test, y_train, y_test = make_train_test(df)

    table, artefacts = compare_models(X_train, y_train, X_test, y_test)
    champion = table.iloc[0]["model"]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    table.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

    joblib.dump(artefacts["models"][champion], MODEL_PATH, compress=3)
    best = table.iloc[0].to_dict()
    metadata = {
        "champion": champion,
        "selection_criterion": "maior ROC-AUC medio na validacao cruzada (5 folds)",
        "threshold": float(artefacts["thresholds"][champion]),
        "features": FEATURES,
        "seed": SEED,
        "sklearn_version": sklearn.__version__,
        "trained_on": date.today().isoformat(),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "metrics": best,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\nCampeao:", champion)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
