from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt

from common import save_plot, setup_output


def funnel_table() -> pd.DataFrame:
    stages = ["广告触达", "查看广告", "点击购买", "提交订单", "支付成功"]
    users = [120000, 42000, 12600, 7560, 6240]
    df = pd.DataFrame({"stage": stages, "users": users})
    df["step_conversion"] = df["users"] / df["users"].shift(1)
    df.loc[0, "step_conversion"] = 1
    df["overall_conversion"] = df["users"] / df.loc[0, "users"]
    df["dropoff"] = 1 - df["step_conversion"]
    return df


def sales_pipeline_table() -> pd.DataFrame:
    stages = ["潜在线索", "初步沟通", "需求确认", "方案报价", "合同签约"]
    opportunities = [950, 520, 310, 160, 86]
    avg_amount = [8000, 9200, 11500, 16800, 22000]
    df = pd.DataFrame({"stage": stages, "opportunities": opportunities, "avg_amount": avg_amount})
    df["weighted_revenue"] = df["opportunities"] * df["avg_amount"]
    df["conversion"] = df["opportunities"] / df["opportunities"].shift(1)
    df.loc[0, "conversion"] = 1
    return df


def plot_funnel(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    y = range(len(df))
    ax.barh(y, df["users"], color="#2F75B5")
    ax.set_yticks(y, df["stage"])
    ax.invert_yaxis()
    ax.set_title("广告用户行为漏斗", loc="left", fontsize=15, fontweight="bold")
    ax.set_xlabel("用户数")
    ax.spines[["top", "right", "left"]].set_visible(False)
    for i, row in df.iterrows():
        ax.text(row["users"], i, f" {row['users']:,} / 总转化 {row['overall_conversion']:.1%}", va="center")
    save_plot(fig, "02_ad_funnel.png")


def plot_sales_pipeline(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(df["stage"], df["opportunities"], marker="o", linewidth=2.5, color="#F28E5B")
    ax.fill_between(df["stage"], df["opportunities"], color="#F28E5B", alpha=0.16)
    ax.set_title("销售漏斗阶段机会数", loc="left", fontsize=15, fontweight="bold")
    ax.set_ylabel("商机数量")
    ax.tick_params(axis="x", rotation=20)
    ax.spines[["top", "right"]].set_visible(False)
    for x, y in zip(df["stage"], df["opportunities"]):
        ax.text(x, y, f"{y}", ha="center", va="bottom")
    save_plot(fig, "02_sales_pipeline.png")


def main() -> None:
    output_dir = setup_output()
    ad_funnel = funnel_table()
    sales_pipeline = sales_pipeline_table()
    ad_funnel.to_csv(output_dir / "02_ad_funnel.csv", index=False, encoding="utf-8-sig")
    sales_pipeline.to_csv(output_dir / "02_sales_pipeline.csv", index=False, encoding="utf-8-sig")
    plot_funnel(ad_funnel)
    plot_sales_pipeline(sales_pipeline)
    print("Funnel experiment completed.")


if __name__ == "__main__":
    main()

