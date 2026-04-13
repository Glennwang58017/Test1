from __future__ import annotations

from .backtest import run_backtest
from .data import load_market_data
from .factors import build_factor_scores
from .portfolio import make_long_short_weights
from .types import PipelineResult, ResearchConfig


def run_research_pipeline(config: ResearchConfig) -> PipelineResult:
    prices = load_market_data(config.data)
    returns = prices.pct_change().fillna(0.0)
    factor_scores = build_factor_scores(prices=prices, config=config.factors)
    weights = make_long_short_weights(
        factor_scores=factor_scores,
        long_quantile=config.portfolio.top_quantile,
        short_quantile=config.portfolio.bottom_quantile,
        rebalance_frequency=config.portfolio.rebalance_frequency,
    )
    backtest = run_backtest(
        weights=weights,
        returns_wide=returns,
        annualization=config.backtest.periods_per_year,
        transaction_cost_bps=config.backtest.transaction_cost_bps,
    )
    return PipelineResult(
        summary=backtest.metrics,
        weights=weights,
        returns=backtest.returns,
        turnover=backtest.turnover,
        equity_curve=backtest.equity_curve,
        factor_scores=factor_scores,
    )
