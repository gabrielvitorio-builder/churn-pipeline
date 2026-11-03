"""Configuracoes centrais do projeto (caminhos, seed e colunas)."""

from pathlib import Path

SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "telco_customer_churn.csv"
MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "churn_model.joblib"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
RESULTS_DIR = ROOT_DIR / "docs" / "results"
FIGURES_DIR = ROOT_DIR / "docs" / "figures"

TARGET = "Churn"
ID_COLUMN = "customerID"

NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]

CATEGORICAL_FEATURES = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Premissas de negocio usadas na metrica de valor (ajustaveis, ver docs/ml_canvas.md)
CUSTOMER_VALUE = 600.0  # receita estimada preservada ao reter um cliente (R$)
RETENTION_COST = 60.0  # custo da acao de retencao por cliente abordado (R$)
RETENTION_SUCCESS_RATE = 0.30  # fracao dos churners abordados que aceita a oferta
