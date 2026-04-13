from __future__ import annotations

import pandas as pd

from .types import PortfolioConfig


def make_long_short_weights(factor_scores: pd.DataFrame, config: PortfolioConfig) -> pd.DataFrame:
    """Build market-neutral weights from wide factor score panel."""
    if factor_scores.empty:
        return pd.DataFrame(index=factor_scores.index, columns=factor_scores.columns).fillna(0.0)

    weight_rows: list[pd.Series] = []

    for date, row in factor_scores.iterrows():
        cs = row.dropna().sort_values()
        if cs.empty:
            continue

        n = len(cs)
        n_long = max(1, int(n * config.top_quantile))
        n_short = max(1, int(n * config.bottom_quantile))
        n_short = min(n_short, n - n_long) if n > n_long else 0

        row = pd.Series(0.0, index=cs.index, name=date)
        if n_long > 0:
            longs = cs.iloc[-n_long:].index
            row.loc[longs] = 1.0 / n_long
        if n_short > 0:
            shorts = cs.iloc[:n_short].index
            row.loc[shorts] = -1.0 / n_short
        weight_rows.append(row)

    if not weight_rows:
        return pd.DataFrame()

    return pd.DataFrame(weight_rows).sort_index().fillna(0.0)
