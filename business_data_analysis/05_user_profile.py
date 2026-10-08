from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def build_users(seed: int = 2026) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    users = pd.DataFrame(
        {
            "user_id": [f"U{idx:04d}" for idx in range(1, 301)],
            "gender": rng.choice(["女", "男"], 300, p=[0.56, 0.44]),
            "age": rng.integers(18, 56, 300),
            "city_tier": rng.choice(["一线", "新一线", "二线", "三线及以下"], 300, p=[0.18, 0.28, 0.32, 0.22]),
            "channel": rng.choice(["搜索", "社交", "短视频", "线下", "转介绍"], 300),
        }
    )
    orders = []
    for user_id in users["user_id"]:
        order_count = int(rng.poisson(2.2))
        for _ in range(order_count):
            orders.append((user_id, rng.choice(["美妆", "数码", "食品", "图书", "运动"]), max(20, rng.gamma(2.5, 70))))
    orders = pd.DataFrame(orders, columns=["user_id", "category", "amount"])
    return users, orders


def build_profile(users: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    spend = orders.groupby("user_id").agg(order_count=("amount", "count"), total_amount=("amount", "sum")).reset_index()
    favorite = (
        orders.groupby(["user_id", "category"]).size().reset_index(name="cnt")
        .sort_values(["user_id", "cnt"], ascending=[True, False])
        .drop_duplicates("user_id")[["user_id", "category"]]
        .rename(columns={"category": "favorite_category"})
    )
    profile = users.merge(spend, on="user_id", how="left").merge(favorite, on="user_id", how="left")
    profile[["order_count", "total_amount"]] = profile[["order_count", "total_amount"]].fillna(0)
    profile["favorite_category"] = profile["favorite_category"].fillna("未购买")
    profile["age_group"] = pd.cut(profile["age"], bins=[17, 25, 35, 45, 60], labels=["18-25", "26-35", "36-45", "46+"])
    profile["value_tag"] = pd.cut(
        profile["total_amount"],
        bins=[-1, 0, 200, 600, float("inf")],
        labels=["未转化", "低价值", "中价值", "高价值"],
    )
    return profile


def plot_profile(profile: pd.DataFrame) -> None:
    pivot = pd.crosstab(profile["age_group"], profile["value_tag"], normalize="index")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bottom = np.zeros(len(pivot))
    colors = ["#EAF0F5", "#AFC2D4", "#2F75B5", "#F28E5B"]
    for idx, col in enumerate(pivot.columns):
        ax.bar(pivot.index.astype(str), pivot[col], bottom=bottom, label=col, color=colors[idx])
        bottom += pivot[col].values
    ax.set_title("年龄层与用户价值标签画像", loc="left", fontsize=15, fontweight="bold")
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
    ax.legend(frameon=False, ncol=4)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "05_user_profile_value_by_age.png")

    channel = pd.crosstab(profile["channel"], profile["value_tag"])
    fig, ax = plt.subplots(figsize=(9, 5.5))
    channel.plot(kind="bar", ax=ax, color=["#AFC2D4", "#21A6A8", "#2F75B5", "#F28E5B"])
    ax.set_title("渠道来源与价值标签", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("渠道")
    ax.set_ylabel("用户数")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    save_plot(fig, "05_user_profile_channel.png")


def main() -> None:
    output_dir = setup_output()
    users, orders = build_users()
    profile = build_profile(users, orders)
    users.to_csv(output_dir / "05_users.csv", index=False, encoding="utf-8-sig")
    orders.to_csv(output_dir / "05_orders.csv", index=False, encoding="utf-8-sig")
    profile.to_csv(output_dir / "05_user_profile.csv", index=False, encoding="utf-8-sig")
    plot_profile(profile)
    print("User profile experiment completed.")


if __name__ == "__main__":
    main()

