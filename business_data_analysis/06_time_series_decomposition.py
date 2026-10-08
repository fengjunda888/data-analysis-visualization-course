from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def build_time_series(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    months = pd.date_range("2023-01-01", periods=36, freq="MS")
    trend = np.linspace(500, 860, len(months))
    seasonal_pattern = np.array([0.92, 0.88, 1.02, 1.06, 1.08, 1.12, 1.04, 0.98, 1.05, 1.13, 1.22, 1.35])
    seasonal = np.tile(seasonal_pattern, 3)
    noise = rng.normal(0, 28, len(months))
    sales = trend * seasonal + noise
    return pd.DataFrame({"month": months, "sales": sales})


def decompose(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["trend"] = result["sales"].rolling(window=6, center=True, min_periods=2).mean()
    result["month_no"] = result["month"].dt.month
    result["seasonal_index"] = result["sales"] / result["trend"]
    seasonal_lookup = result.groupby("month_no")["seasonal_index"].mean()
    result["seasonal"] = result["month_no"].map(seasonal_lookup)
    result["deseasonalized"] = result["sales"] / result["seasonal"]
    result["residual"] = result["sales"] - result["trend"] * result["seasonal"]
    return result


def simple_forecast(decomposed: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    valid = decomposed.dropna(subset=["deseasonalized"]).copy()
    x = np.arange(len(valid))
    slope, intercept = np.polyfit(x, valid["deseasonalized"], 1)
    future_months = pd.date_range(decomposed["month"].max() + pd.offsets.MonthBegin(1), periods=periods, freq="MS")
    seasonal_lookup = decomposed.groupby("month_no")["seasonal"].mean()
    future_x = np.arange(len(valid), len(valid) + periods)
    future = pd.DataFrame({"month": future_months})
    future["month_no"] = future["month"].dt.month
    future["trend_forecast"] = intercept + slope * future_x
    future["seasonal"] = future["month_no"].map(seasonal_lookup)
    future["forecast_sales"] = future["trend_forecast"] * future["seasonal"]
    return future


def plot_series(decomposed: pd.DataFrame, forecast: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(decomposed["month"], decomposed["sales"], label="实际销售额", color="#2F75B5", marker="o")
    ax.plot(decomposed["month"], decomposed["trend"], label="趋势项", color="#F28E5B", linewidth=2.5)
    ax.plot(forecast["month"], forecast["forecast_sales"], label="预测销售额", color="#21A6A8", marker="o", linestyle="--")
    ax.set_title("效应分解法时间序列预测", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("销售额")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "06_time_series_forecast.png")

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(decomposed["month"], decomposed["trend"], color="#F28E5B")
    axes[0].set_title("趋势项", loc="left")
    axes[1].plot(decomposed["month"], decomposed["seasonal"], color="#21A6A8")
    axes[1].set_title("季节项", loc="left")
    axes[2].plot(decomposed["month"], decomposed["residual"], color="#7B61A8")
    axes[2].axhline(0, color="#AFC2D4", linewidth=1)
    axes[2].set_title("残差项", loc="left")
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "06_time_series_components.png")


def main() -> None:
    output_dir = setup_output()
    df = build_time_series()
    decomposed = decompose(df)
    forecast = simple_forecast(decomposed)
    decomposed.to_csv(output_dir / "06_time_series_decomposition.csv", index=False, encoding="utf-8-sig")
    forecast.to_csv(output_dir / "06_time_series_forecast.csv", index=False, encoding="utf-8-sig")
    plot_series(decomposed, forecast)
    print("Time series experiment completed.")


if __name__ == "__main__":
    main()

