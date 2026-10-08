# 《商业数据分析》Python 实验迁移说明

资料来源：`CDA一级认证教材 商业数据分析（第4版）_9787121504884_og2025.pdf`

## 迁移原则

教材中的内容分为三类处理：

1. 理论框架：整理为实验说明，不逐字复制教材内容。
2. Excel / Power BI / SQL 案例：理解其分析目标、指标逻辑和图表表达方式，迁移为 Python 可运行脚本。
3. Python Notebook：当前目录中未发现 `.ipynb` 文件，因此暂未执行 Notebook 到 `.py` 的转换。

由于当前只提供 PDF 教材，未提供配套数据包、`.pbix` 或 Notebook 文件，因此本实验使用可复现的模拟数据来呈现教材中的分析方法。脚本重点体现分析流程、指标计算和可视化结果，不声称复刻教材原始数据。

## 已迁移实验

| 序号 | Python 文件 | 对应教材主题 | 原工具/场景 | Python 迁移内容 |
| --- | --- | --- | --- | --- |
| 1 | `business_data_analysis/01_rfm_model.py` | RFM 用户价值分析 | Excel/BI 分群 | 构造订单数据、计算 R/F/M、用户分层、输出分层图 |
| 2 | `business_data_analysis/02_funnel_analysis.py` | 漏斗分析模型 | Excel/BI 漏斗图 | 广告漏斗、销售漏斗、转化率和流失率计算 |
| 3 | `business_data_analysis/03_cohort_retention.py` | 同期群分析 | Excel/BI 留存报表 | 构造注册留存数据、生成留存率矩阵和趋势图 |
| 4 | `business_data_analysis/04_descriptive_statistics.py` | 描述性统计分析 | 表格统计 | 均值、中位数、标准差、置信区间、分布图 |
| 5 | `business_data_analysis/05_user_profile.py` | 用户画像 | SQL + Excel | 用户标签加工、价值标签、渠道与年龄画像 |
| 6 | `business_data_analysis/06_time_series_decomposition.py` | 简单时间序列分析 | Power BI 效应分解 | 趋势项、季节项、残差项、简易预测 |

## 运行方式

单独运行某个实验：

```powershell
python business_data_analysis/01_rfm_model.py
```

一次运行全部《商业数据分析》实验：

```powershell
python run_business_data_analysis.py
```

输出结果位于：

```text
business_data_analysis_outputs/
```

包括 CSV 过程数据和 PNG 图表结果。

## 与教材要求的对应

### Excel / Power BI 实现迁移为 Python

已完成：

- RFM 用户价值分析
- 漏斗分析
- 同期群留存分析
- 用户画像
- 时间序列效应分解
- 描述性统计

### Notebook 转 `.py`

当前未完成。原因：项目目录中没有 `.ipynb` 文件。

如后续提供 Notebook 文件，可继续执行：

1. 读取 Notebook 的代码单元。
2. 合并并整理为 `.py` 文件。
3. 将 Markdown 说明改写为函数注释或实验文档。
4. 验证脚本可以从命令行运行。

## 后续可扩展

如果提供教材配套数据，可以把当前模拟数据替换为真实数据，并保留同样的计算逻辑和输出结构。

