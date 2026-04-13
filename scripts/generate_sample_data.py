from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_prices(n_months: int = 120, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2016-01-31", periods=n_months, freq="ME")
    assets = [
        ("SPY_US", "US", "Equity"),
        ("QQQ_US", "US", "Equity"),
        ("IEUR_EU", "EU", "Equity"),
        ("EWJ_JP", "JP", "Equity"),
        ("MCHI_CN", "CN", "Equity"),
        ("INDA_IN", "IN", "Equity"),
        ("EWZ_BR", "BR", "Equity"),
        ("EWA_AU", "AU", "Equity"),
        ("EWU_UK", "UK", "Equity"),
        ("EWC_CA", "CA", "Equity"),
    ]
    records: list[dict[str, object]] = []

    for idx, (asset, region, _sector) in enumerate(assets):
        drift = 0.005 + 0.0004 * (idx % 5)
        vol = 0.03 + 0.003 * (idx % 4)
        rets = rng.normal(loc=drift, scale=vol, size=n_months)
        price = 100 * np.cumprod(1 + rets)
        for date, p in zip(dates, price):
            records.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "asset": asset,
                    "region": region,
                    "close": float(p),
                }
            )

    return pd.DataFrame(records)


def main() -> None:
    out_path = Path("data/sample/global_prices_sample.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_prices()
    df.to_csv(out_path, index=False)
    print(f"Generated sample data: {out_path} ({len(df)} rows)")


if __name__ == "__main__":
    main()
