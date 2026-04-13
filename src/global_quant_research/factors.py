"""Factor construction for cross-sectional global equities research."""

from __future__ import annotations

import pandas as pd


def compute_features(
    prices: pd.DataFrame,
    lookback_momentum: int,
    lookback_reversal: int,
    lookback_volatility: int,
) -> pd.DataFrame:
    """Return MultiIndex factor features indexed by (date, asset)."""
    returns = prices.pct_change()
    momentum = prices.pct_change(lookback_momentum)
    reversal = -prices.pct_change(lookback_reversal)
    volatility = returns.rolling(lookback_volatility).std()

    features = (
        momentum.stack().rename("momentum").to_frame()
        .join(reversal.stack().rename("reversal").to_frame(), how="outer")
        .join(volatility.stack().rename("volatility").to_frame(), how="outer")
    )
    return features.dropna().sort_index()


def composite_signal(features: pd.DataFrame) -> pd.Series:
    """Build a simple standardized composite score from raw factors."""
    out = features.copy()
    for col in ["momentum", "reversal", "volatility"]:
        cs_mean = out[col].groupby(level=0).transform("mean")
        cs_std = out[col].groupby(level=0).transform("std").replace(0.0, pd.NA)
        out[col] = (out[col] - cs_mean) / cs_std
    score = out["momentum"] + out["reversal"] - out["volatility"]
    return score.fillna(0.0).rename("score")

