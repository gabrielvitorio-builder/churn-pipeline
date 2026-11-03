"""Ponto de entrada para o deploy na Vercel (funcao serverless Python)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from churn_api.main import app  # noqa: E402,F401
