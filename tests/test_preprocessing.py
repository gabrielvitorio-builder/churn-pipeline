import numpy as np
import pandas as pd

from churn.config import FEATURES, ID_COLUMN, TARGET
from churn.data import clean_data, load_raw_data, make_train_test
from churn.preprocessing import build_preprocessor


def test_clean_data_converts_total_charges_and_target():
    raw = load_raw_data()
    df = clean_data(raw)
    assert pd.api.types.is_numeric_dtype(df["TotalCharges"])
    assert df["TotalCharges"].isna().sum() == 11
    assert set(df[TARGET].unique()) == {0, 1}
    assert ID_COLUMN not in df.columns
    assert len(df) == len(raw)


def test_preprocessor_outputs_numeric_matrix_without_nan():
    df = clean_data(load_raw_data())
    X = df[FEATURES]
    out = build_preprocessor().fit_transform(X)
    assert out.shape[0] == len(X)
    assert out.shape[1] > len(FEATURES)  # one-hot expande as categoricas
    assert not np.isnan(out.toarray() if hasattr(out, "toarray") else out).any()


def test_preprocessor_ignores_unseen_category():
    df = clean_data(load_raw_data())
    X = df[FEATURES]
    prep = build_preprocessor().fit(X)
    novel = X.head(1).copy()
    novel["Contract"] = "Categoria nova"
    out = prep.transform(novel)
    assert out.shape[0] == 1


def test_train_test_split_is_reproducible_and_stratified():
    df = clean_data(load_raw_data())
    a = make_train_test(df)
    b = make_train_test(df)
    assert a[0].index.equals(b[0].index)
    assert abs(a[2].mean() - a[3].mean()) < 0.01
