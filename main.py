"""Compatibility entry point for `uvicorn main:app`."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from api.main import app  # noqa: E402, F401
