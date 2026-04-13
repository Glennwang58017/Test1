from __future__ import annotations

import numpy as np
import pandas as pd

from .types import BacktestOutput


def _annualized_return(period_returns: pd.Series, annualization: int) -> float:
    if period_returns.empty:
        return 0.0
    compounded = float((1.0 + period_returns).prod())
    years = len(period_returns) / annualization
    if years <= 0:
        return 0.0
    return compounded ** (1.0 / years) - 1.0


def _annualized_volatility(period_returns: pd.Series, annualization: int) -> float:
    if period_returns.empty:
        return 0.0
    return float(period_returns.std(ddof=0) * np.sqrt(annualization))


def _max_drawdown(equity_curve: pd.Series) -> float:
    if equity_curve.empty:
        return 0.0
    rolling_peak = equity_curve.cummax()
    drawdown = equity_curve / rolling_peak - 1.0
    return float(drawdown.min())


def run_backtest(
    *,
    weights: pd.DataFrame,
    returns_wide: pd.DataFrame,
    annualization: int,
    transaction_cost_bps: float,
) -> BacktestOutput:
    aligned_weights = weights.reindex(index=returns_wide.index).fillna(0.0)
    shifted_weights = aligned_weights.shift(1).fillna(0.0)
    gross_returns = (shifted_weights * returns_wide).sum(axis=1)

    turnover = aligned_weights.diff().abs().sum(axis=1).fillna(0.0)
    cost = turnover * (transaction_cost_bps / 10_000.0)
    net_returns = gross_returns - cost

    equity_curve = (1.0 + net_returns).cumprod()
    ann_return = _annualized_return(net_returns, annualization)
    ann_vol = _annualized_volatility(net_returns, annualization)
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0.0

    metrics = {
        "cumulative_return": float(equity_curve.iloc[-1] - 1.0) if not equity_curve.empty else 0.0,
        "annualized_return": ann_return,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": sharpe,
        "max_drawdown": _max_drawdown(equity_curve),
        "win_rate": float((net_returns > 0).mean()) if not net_returns.empty else 0.0,
        "average_turnover": float(turnover.mean()) if not turnover.empty else 0.0,
    }

    return BacktestOutput(
        returns=net_returns,
        turnover=turnover,
        equity_curve=equity_curve,
        metrics=metrics,
    )
