"""API REST de inferencia de churn.

Execucao local:
    uvicorn churn_api.main:app --reload --app-dir src
"""

from __future__ import annotations

import sys
from pathlib import Path

# Garante que `churn` e `churn_api` sejam importaveis quando o modulo e carregado
# pelo caminho completo (src.churn_api.main), como faz a Vercel.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException  # noqa: E402

from churn.predict import (  # noqa: E402
    ModelNotAvailableError,
    load_metadata,
    load_model,
    predict_customer,
)
from churn_api.schemas import CustomerInput, HealthOutput, PredictionOutput  # noqa: E402

app = FastAPI(
    title="Churn Prediction API",
    description="Classifica o risco de cancelamento de clientes de telecomunicacoes.",
    version="0.1.0",
)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "Churn Prediction API. Veja /docs, /health e /predict."}


@app.get("/health", response_model=HealthOutput)
def health() -> HealthOutput:
    """Informa se a API esta no ar e se o modelo foi carregado."""
    try:
        load_model()
        name = load_metadata().get("champion")
        return HealthOutput(status="ok", model_loaded=True, model=name)
    except ModelNotAvailableError:
        return HealthOutput(status="degraded", model_loaded=False)


@app.post("/predict", response_model=PredictionOutput)
def predict(customer: CustomerInput) -> PredictionOutput:
    """Recebe os dados de um cliente e retorna a propensao de churn."""
    try:
        result = predict_customer(customer.model_dump())
    except ModelNotAvailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return PredictionOutput(**result)
