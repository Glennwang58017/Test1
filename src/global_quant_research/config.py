from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .types import BacktestConfig, DataConfig, FactorConfig, PortfolioConfig, ResearchConfig


def load_config(path: str | Path) -> ResearchConfig:
    with Path(path).open("r", encoding="utf-8") as file:
        raw: dict[str, Any] = yaml.safe_load(file)

    data = raw["data"]
    factors = raw["factors"]
    portfolio = raw["portfolio"]
    backtest = raw["backtest"]

    return ResearchConfig(
        data=DataConfig(
            csv_path=data["csv_path"],
            date_col=data["date_col"],
            asset_col=data["asset_col"],
            price_col=data["price_col"],
        ),
        factors=FactorConfig(
            momentum_window=factors["momentum_window"],
            short_reversal_window=factors["short_reversal_window"],
            volatility_window=factors["volatility_window"],
            normalize_cross_sectional=factors["normalize_cross_sectional"],
        ),
        portfolio=PortfolioConfig(
            top_quantile=portfolio["top_quantile"],
            bottom_quantile=portfolio["bottom_quantile"],
            rebalance_frequency=portfolio["rebalance_frequency"],
        ),
        backtest=BacktestConfig(
            periods_per_year=backtest["periods_per_year"],
            transaction_cost_bps=backtest.get("transaction_cost_bps", 0.0),
        ),
    )
