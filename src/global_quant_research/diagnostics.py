from __future__ import annotations

import pandas as pd

from .types import FactorDiagnostics


def _cross_sectional_corr(
    factor_scores: pd.DataFrame,
    forward_returns: pd.DataFrame,
    *,
    method: str,
) -> pd.Series:
    values: dict[pd.Timestamp, float] = {}
    for date in factor_scores.index.intersection(forward_returns.index):
        score = factor_scores.loc[date]
        fwd = forward_returns.loc[date]
        joined = pd.concat([score, fwd], axis=1, keys=["score", "fwd"]).dropna()
        if len(joined) < 2:
            continue
        if method == "spearman":
            corr = joined["score"].rank().corr(joined["fwd"].rank(), method="pearson")
        else:
            corr = joined["score"].corr(joined["fwd"], method=method)
        if pd.notna(corr):
            values[date] = float(corr)
    return pd.Series(values).sort_index()


def _quantile_labels(row: pd.Series, n_quantiles: int) -> pd.Series:
    valid = row.dropna()
    if valid.empty:
        return pd.Series(index=row.index, dtype=float)
    ranked = valid.rank(method="first")
    labels = pd.qcut(ranked, q=n_quantiles, labels=False) + 1
    out = pd.Series(index=row.index, dtype=float)
    out.loc[labels.index] = labels.astype(float)
    return out


def run_factor_diagnostics(
    *,
    factor_scores: pd.DataFrame,
    returns_wide: pd.DataFrame,
    quantiles: int = 5,
) -> FactorDiagnostics:
    """Compute basic factor research diagnostics."""
    forward_returns = returns_wide.shift(-1)
    ic_series = _cross_sectional_corr(
        factor_scores=factor_scores,
        forward_returns=forward_returns,
        method="pearson",
    )
    rank_ic_series = _cross_sectional_corr(
        factor_scores=factor_scores,
        forward_returns=forward_returns,
        method="spearman",
    )

    quantile_map = factor_scores.apply(_quantile_labels, axis=1, n_quantiles=quantiles)
    quantile_returns: dict[int, pd.Series] = {}
    for q in range(1, quantiles + 1):
        q_mask = quantile_map.eq(float(q))
        q_ret = forward_returns.where(q_mask).mean(axis=1, skipna=True)
        quantile_returns[q] = q_ret
    quantile_returns_df = pd.DataFrame(quantile_returns).dropna(how="all")
    quantile_cumulative_df = (1.0 + quantile_returns_df.fillna(0.0)).cumprod() - 1.0

    spread_returns = pd.Series(dtype=float)
    if not quantile_returns_df.empty and 1 in quantile_returns_df and quantiles in quantile_returns_df:
        spread_returns = quantile_returns_df[quantiles] - quantile_returns_df[1]

    summary = {
        "mean_ic": float(ic_series.mean()) if not ic_series.empty else 0.0,
        "mean_rank_ic": float(rank_ic_series.mean()) if not rank_ic_series.empty else 0.0,
        "ic_ir": float(ic_series.mean() / ic_series.std(ddof=0))
        if len(ic_series) > 1 and ic_series.std(ddof=0)
        else 0.0,
        "rank_ic_ir": float(rank_ic_series.mean() / rank_ic_series.std(ddof=0))
        if len(rank_ic_series) > 1 and rank_ic_series.std(ddof=0)
        else 0.0,
        "mean_quantile_spread": float(spread_returns.mean()) if not spread_returns.empty else 0.0,
    }

    return FactorDiagnostics(
        summary=summary,
        ic_series=ic_series,
        rank_ic_series=rank_ic_series,
        quantile_returns=quantile_returns_df,
        quantile_cumulative_returns=quantile_cumulative_df,
        quantile_spread=spread_returns.dropna(),
    )
