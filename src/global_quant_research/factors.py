"""Factor construction for cross-sectional global equities research."""

from __future__ import annotations

import pandas as pd

from .types import FactorConfig


def _zscore_rowwise(df: pd.DataFrame) -> pd.DataFrame:
    mean = df.mean(axis=1)
    std = df.std(axis=1).replace(0.0, pd.NA)
    return df.sub(mean, axis=0).div(std, axis=0)


def build_factor_scores(prices: pd.DataFrame, config: FactorConfig) -> pd.DataFrame:
    """Build composite cross-sectional factor scores in wide format."""
    returns = prices.pct_change()
    momentum = prices.pct_change(config.momentum_window)
    reversal = -prices.pct_change(config.short_reversal_window)
    volatility = returns.rolling(config.volatility_window).std()

    if config.normalize_cross_sectional:
        momentum = _zscore_rowwise(momentum)
        reversal = _zscore_rowwise(reversal)
        volatility = _zscore_rowwise(volatility)

    score = momentum + reversal - volatility
    return score.dropna(how="all")

