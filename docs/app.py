"""Ponto de entrada para o deploy na Vercel (FastAPI com `app` na raiz)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fastapi import FastAPI  # noqa: E402

from churn_api.main import app  # noqa: E402

assert isinstance(app, FastAPI)