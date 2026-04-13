# 全球量化模型研究项目（Global Quant Research）

这是一个可直接运行的“全球量化研究”项目骨架，适合用于：

- 因子研究（动量 / 反转 / 波动率）
- 全球资产池截面选股
- 多空组合构建
- 含换手成本的简化回测
- 快速扩展到你自己的数据与因子

## 项目结构

```text
.
├── configs/
│   └── research.yaml              # 研究配置
├── data/
│   └── sample/
│       └── global_prices_sample.csv  # 示例全球价格数据（月频）
├── scripts/
│   └── generate_sample_data.py    # 生成示例数据脚本
├── src/
│   └── global_quant_research/
│       ├── __init__.py
│       ├── __main__.py
│       ├── backtest.py            # 回测与绩效指标
│       ├── config.py              # 配置加载
│       ├── data.py                # 数据读取与清洗
│       ├── factors.py             # 因子构建
│       ├── pipeline.py            # 研究流水线
│       ├── portfolio.py           # 组合构建与调仓
│       ├── run.py                 # 命令行运行入口
│       └── types.py               # 数据类型定义
└── tests/
    └── test_pipeline.py           # 基础测试
```

## 快速开始

### 1) 安装依赖

```bash
python3 -m pip install -e ".[dev]"
```

### 2) 运行研究流水线

```bash
python3 -m global_quant_research
```

运行后会输出策略关键指标（累计收益、年化收益、波动率、夏普、最大回撤、胜率、平均换手等）以及最近一期权重。

### 3) 重新生成样本数据（可选）

```bash
python3 scripts/generate_sample_data.py
```

## 配置说明（configs/research.yaml）

- `data`: 数据路径与列名映射
- `factors`:
  - `momentum_window`: 动量窗口
  - `short_reversal_window`: 短期反转窗口
  - `volatility_window`: 波动率窗口
  - `normalize_cross_sectional`: 是否做截面标准化
- `portfolio`:
  - `top_quantile`: 做多分位数
  - `bottom_quantile`: 做空分位数
  - `rebalance_frequency`: 调仓频率（例如 `M`）
- `backtest`:
  - `periods_per_year`: 年化换算周期（月频用 12，日频用 252）
  - `transaction_cost_bps`: 单边交易成本（基点）

## 下一步可扩展方向

1. 接入真实多市场日频数据（股票/ETF/期货）
2. 增加行业/国家中性约束与风格暴露控制
3. 引入多因子 IC 分析、分层回测与归因
4. 增加 walk-forward / rolling OOS 验证
5. 对接向量数据库或研究平台进行因子版本管理
