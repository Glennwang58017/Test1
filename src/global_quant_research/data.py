from __future__ import annotations

from pathlib import Path

import pandas as pd

from .types import DataConfig


def load_market_data(cfg: DataConfig) -> pd.DataFrame:
    """Load long-format price data and return wide price panel (date x asset)."""
    csv_path = Path(cfg.csv_path)
    df = pd.read_csv(csv_path)
    expected = {cfg.date_col, cfg.asset_col, cfg.price_col}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = df[[cfg.date_col, cfg.asset_col, cfg.price_col]].copy()
    data[cfg.date_col] = pd.to_datetime(data[cfg.date_col])
    data = data.sort_values([cfg.date_col, cfg.asset_col])

    panel = data.pivot(index=cfg.date_col, columns=cfg.asset_col, values=cfg.price_col).sort_index()
    return panel
