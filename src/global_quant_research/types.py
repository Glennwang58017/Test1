from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DataConfig:
    csv_path: str
    date_col: str
    asset_col: str
    price_col: str


@dataclass(frozen=True)
class FactorConfig:
    momentum_window: int
    short_reversal_window: int
    volatility_window: int
    normalize_cross_sectional: bool = True


@dataclass(frozen=True)
class PortfolioConfig:
    top_quantile: float
    bottom_quantile: float
    rebalance_frequency: str


@dataclass(frozen=True)
class BacktestConfig:
    periods_per_year: int
    transaction_cost_bps: float = 0.0


@dataclass(frozen=True)
class ResearchConfig:
    data: DataConfig
    factors: FactorConfig
    portfolio: PortfolioConfig
    backtest: BacktestConfig


@dataclass(frozen=True)
class BacktestOutput:
    returns: pd.Series
    turnover: pd.Series
    equity_curve: pd.Series
    metrics: dict[str, float]


@dataclass(frozen=True)
class FactorDiagnostics:
    summary: dict[str, float]
    ic_series: pd.Series
    rank_ic_series: pd.Series
    quantile_returns: pd.DataFrame
    quantile_cumulative_returns: pd.DataFrame
    quantile_spread: pd.Series


@dataclass(frozen=True)
class ResearchOutput:
    summary: dict[str, float]
    returns: pd.Series
    equity_curve: pd.Series
    turnover: pd.Series
    weights: pd.DataFrame
    factor_scores: pd.DataFrame
    diagnostics: FactorDiagnostics
