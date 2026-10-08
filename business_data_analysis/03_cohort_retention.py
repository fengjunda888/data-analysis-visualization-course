from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def build_retention(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    cohorts = pd.date_range("2026-03-06", periods=7, freq="D")
    rows = []
    for i, cohort in enumerate(cohorts):
        new_users = int(rng.integers(760, 1300))
        activity_boost = 0.08 if cohort.day == 8 else 0
        for day_n in range(8):
            base_rate = max(0.08, 0.72 * np.exp(-0.33 * day_n))
            rate = min(0.92, base_rate + activity_boost - i * 0.01 + rng.normal(0, 0.018))
            retained = int(new_users * max(rate, 0.03))
            rows.append((cohort.date(), day_n, new_users, retained, retained / new_users))
    return pd.DataFrame(rows, columns=["cohort_date", "day_n", "new_users", "retained_users", "retention_rate"])


def plot_retention(df: pd.DataFrame) -> None:
    matrix = df.pivot(index="cohort_date", columns="day_n", values="retention_rate")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    im = ax.imshow(matrix.values, cmap="YlGnBu", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(matrix.shape[1]), [f"D+{c}" for c in matrix.columns])
    ax.set_yticks(range(matrix.shape[0]), [str(i) for i in matrix.index])
    ax.set_title("同期群留存率热力图", loc="left", fontsize=15, fontweight="bold")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix.iloc[i, j]:.0%}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    save_plot(fig, "03_cohort_retention_heatmap.png")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for cohort, group in df.groupby("cohort_date"):
        ax.plot(group["day_n"], group["retention_rate"], marker="o", linewidth=1.8, label=str(cohort))
    ax.set_title("同期群用户留存趋势", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("注册后的第 N 日")
    ax.set_ylabel("留存率")
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
    ax.legend(frameon=False, fontsize=8, ncol=2)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "03_cohort_retention_trend.png")


def main() -> None:
    output_dir = setup_output()
    df = build_retention()
    df.to_csv(output_dir / "03_cohort_retention.csv", index=False, encoding="utf-8-sig")
    plot_retention(df)
    print("Cohort experiment completed.")


if __name__ == "__main__":
    main()

