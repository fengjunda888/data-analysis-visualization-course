from __future__ import annotations

import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def build_sales(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    regions = ["华北", "华东", "华南", "西南"]
    products = ["基础版", "专业版", "旗舰版"]
    rows = []
    for region in regions:
        for product in products:
            for month in pd.period_range("2025-01", "2025-12", freq="M"):
                base = {"基础版": 80, "专业版": 135, "旗舰版": 210}[product]
                region_factor = {"华北": 1.00, "华东": 1.18, "华南": 1.08, "西南": 0.88}[region]
                sales = rng.normal(base * region_factor, 18)
                rows.append((str(month), region, product, max(round(sales, 2), 20)))
    return pd.DataFrame(rows, columns=["month", "region", "product", "sales"])


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["region", "product"])["sales"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )
    summary["se"] = summary["std"] / np.sqrt(summary["count"])
    summary["ci95_low"] = summary["mean"] - 1.96 * summary["se"]
    summary["ci95_high"] = summary["mean"] + 1.96 * summary["se"]
    return summary


def plot_stats(df: pd.DataFrame, summary: pd.DataFrame) -> None:
    region_summary = df.groupby("region")["sales"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(region_summary.index, region_summary.values, color="#21A6A8")
    ax.set_title("各区域平均销售额", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("平均销售额")
    ax.spines[["top", "right"]].set_visible(False)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{bar.get_height():.1f}", ha="center", va="bottom")
    save_plot(fig, "04_region_mean_sales.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["sales"], bins=18, color="#2F75B5", alpha=0.82)
    ax.axvline(df["sales"].mean(), color="#F28E5B", linestyle="--", linewidth=2, label=f"均值 {df['sales'].mean():.1f}")
    ax.set_title("销售额分布", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("销售额")
    ax.set_ylabel("频数")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "04_sales_distribution.png")


def main() -> None:
    output_dir = setup_output()
    df = build_sales()
    summary = summarize(df)
    df.to_csv(output_dir / "04_sales_data.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(output_dir / "04_descriptive_summary.csv", index=False, encoding="utf-8-sig")
    plot_stats(df, summary)
    print("Descriptive statistics experiment completed.")


if __name__ == "__main__":
    main()

