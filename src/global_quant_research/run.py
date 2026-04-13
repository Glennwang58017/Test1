from __future__ import annotations

from pathlib import Path

from .config import load_config
from .pipeline import run_research_pipeline


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "configs" / "research.yaml"
    config = load_config(config_path)
    result = run_research_pipeline(config)

    print("=== Global Quant Research Result ===")
    for k, v in result.metrics.items():
        print(f"{k}: {v:.6f}")
    print("\nLatest portfolio weights:")
    print(result.weights.tail(10).to_string())


if __name__ == "__main__":
    main()
