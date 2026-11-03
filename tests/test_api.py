from fastapi.testclient import TestClient

from churn_api.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


def test_predict_returns_probability(sample_customer):
    response = client.post("/predict", json=sample_customer)
    assert response.status_code == 200
    body = response.json()
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert body["risk_level"] in {"baixo", "medio", "alto"}


def test_high_risk_profile_scores_above_low_risk_profile(sample_customer):
    low = dict(
        sample_customer,
        tenure=60,
        Contract="Two year",
        InternetService="DSL",
        MonthlyCharges=40.0,
        TotalCharges=2400.0,
        PaymentMethod="Bank transfer (automatic)",
        OnlineSecurity="Yes",
        TechSupport="Yes",
    )
    high = client.post("/predict", json=sample_customer).json()["churn_probability"]
    low_p = client.post("/predict", json=low).json()["churn_probability"]
    assert high > low_p


def test_predict_rejects_invalid_payload(sample_customer):
    bad = dict(sample_customer, Contract="Contrato inexistente")
    assert client.post("/predict", json=bad).status_code == 422
    missing = {k: v for k, v in sample_customer.items() if k != "tenure"}
    assert client.post("/predict", json=missing).status_code == 422
