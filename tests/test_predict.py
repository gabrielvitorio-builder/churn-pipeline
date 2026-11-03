from churn.predict import predict_customer, risk_level


def test_predict_customer_returns_valid_output(sample_customer):
    result = predict_customer(sample_customer)
    assert 0.0 <= result["churn_probability"] <= 1.0
    assert result["risk_level"] in {"baixo", "medio", "alto"}
    assert result["churn_prediction"] == (result["churn_probability"] >= result["threshold"])


def test_predict_accepts_missing_total_charges(sample_customer):
    sample_customer["TotalCharges"] = None
    result = predict_customer(sample_customer)
    assert 0.0 <= result["churn_probability"] <= 1.0


def test_risk_level_bands():
    assert risk_level(0.2, 0.45) == "baixo"
    assert risk_level(0.5, 0.45) == "medio"
    assert risk_level(0.9, 0.45) == "alto"
