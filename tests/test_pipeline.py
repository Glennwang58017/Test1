from pathlib import Path

import pandas as pd

from global_quant_research.config import load_config
from global_quant_research.pipeline import run_research_pipeline


def test_pipeline_runs_with_sample_data() -> None:
    config = load_config(Path("configs/research.yaml"))
    output = run_research_pipeline(config)

    assert output.summary["annualized_volatility"] > 0
    assert "cumulative_return" in output.summary
    assert output.summary["number_of_rebalance_dates"] > 0
    assert not output.weights.empty
    assert "mean_ic" in output.diagnostics.summary
    assert "mean_rank_ic" in output.diagnostics.summary
    assert not output.diagnostics.ic_series.empty
    assert not output.diagnostics.rank_ic_series.empty
    assert not output.diagnostics.quantile_returns.empty


def test_sample_data_has_required_columns() -> None:
    data = pd.read_csv("data/sample/global_prices_sample.csv")
    required = {"date", "asset", "region", "close"}
    assert required.issubset(set(data.columns))
