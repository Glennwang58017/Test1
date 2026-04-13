"""Global quantitative research starter package."""

from .pipeline import run_research_pipeline
from .diagnostics import run_factor_diagnostics

__all__ = ["run_research_pipeline", "run_factor_diagnostics"]
