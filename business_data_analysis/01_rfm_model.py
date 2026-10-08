from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def build_orders(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    customer_ids = [f"C{idx:03d}" for idx in range(1, 81)]
    rows = []
    start = datetime(2026, 1, 1)
    for cid in customer_ids:
        order_count = int(rng.integers(1, 12))
        for _ in range(order_count):
            order_date = start + timedelta(days=int(rng.integers(0, 180)))
            amount = round(float(rng.gamma(shape=2.8, scale=95) + rng.normal(0, 15)), 2)
            rows.append((cid, order_date, max(amount, 20)))
    return pd.DataFrame(rows, columns=["customer_id", "order_date", "amount"])


def score_rfm(orders: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = orders["order_date"].max() + pd.Timedelta(days=1)
    rfm = (
        orders.groupby("customer_id")
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_date", "count"),
            monetary=("amount", "sum"),
        )
        .reset_index()
    )
    rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
    rfm["rfm_score"] = rfm[["r_score", "f_score", "m_score"]].sum(axis=1)
    conditions = [
        (rfm["r_score"] >= 3) & (rfm["f_score"] >= 3) & (rfm["m_score"] >= 3),
        (rfm["r_score"] >= 3) & (rfm["f_score"] <= 2),
        (rfm["r_score"] <= 2) & (rfm["m_score"] >= 3),
        (rfm["r_score"] <= 2) & (rfm["f_score"] <= 2),
    ]
    choices = ["重要价值用户", "新近潜力用户", "重要挽回用户", "一般/沉睡用户"]
    rfm["segment"] = np.select(conditions, choices, default="普通保持用户")
    return rfm


def plot_segments(rfm: pd.DataFrame) -> None:
    segment_counts = rfm["segment"].value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(segment_counts.index, segment_counts.values, color="#2F75B5")
    ax.set_title("RFM 用户分层", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("用户数")
    ax.tick_params(axis="x", rotation=25)
    ax.spines[["top", "right"]].set_visible(False)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), int(bar.get_height()), ha="center", va="bottom")
    save_plot(fig, "01_rfm_segments.png")

    fig, ax = plt.subplots(figsize=(8, 6))
    for segment, data in rfm.groupby("segment"):
        ax.scatter(data["recency"], data["monetary"], s=data["frequency"] * 18, alpha=0.72, label=segment)
    ax.set_title("RFM 三指标关系", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("Recency: 最近消费间隔天数，越小越活跃")
    ax.set_ylabel("Monetary: 累计消费金额")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "01_rfm_scatter.png")


def main() -> None:
    output_dir = setup_output()
    orders = build_orders()
    rfm = score_rfm(orders)
    orders.to_csv(output_dir / "01_rfm_orders.csv", index=False, encoding="utf-8-sig")
    rfm.to_csv(output_dir / "01_rfm_result.csv", index=False, encoding="utf-8-sig")
    plot_segments(rfm)
    print("RFM experiment completed.")


if __name__ == "__main__":
    main()

