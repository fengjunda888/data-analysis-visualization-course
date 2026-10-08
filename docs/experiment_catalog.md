# 实验目录与迁移清单

## 一、课程要求对应关系

### 1. Excel / Power BI 案例迁移为 Python

当前已处理：

| 课程 | 教材/资料 | 原实现方式 | Python 文件 | 状态 |
| --- | --- | --- | --- | --- |
| 大数据分析及数据可视化 | 《Excel数据可视化——从图表到数据大屏》第二章 | Excel 图表 | `reproduce_chapter2_charts.py` | 已完成 |
| 商业数据分析 | RFM 用户价值分析 | Excel/BI 分群 | `business_data_analysis/01_rfm_model.py` | 已完成 |
| 商业数据分析 | 漏斗分析 | Excel/BI 漏斗图 | `business_data_analysis/02_funnel_analysis.py` | 已完成 |
| 商业数据分析 | 同期群分析 | Excel/BI 留存报表 | `business_data_analysis/03_cohort_retention.py` | 已完成 |
| 商业数据分析 | 描述性统计分析 | 表格统计 | `business_data_analysis/04_descriptive_statistics.py` | 已完成 |
| 商业数据分析 | 用户画像 | SQL + Excel | `business_data_analysis/05_user_profile.py` | 已完成 |
| 商业数据分析 | 时间序列效应分解 | Power BI | `business_data_analysis/06_time_series_decomposition.py` | 已完成 |

待处理：

| 课程 | 资料 | 状态 |
| --- | --- | --- |
| 商业数据分析 | 配套真实数据集 | 当前使用模拟数据，等待提供配套数据后替换 |
| 商业数据分析 | `.pbix` 文件 | 等待提供后可进一步复刻 Power BI 页面结构 |
| 大数据分析及数据可视化 | 《Excel数据可视化——从图表到数据大屏》后续章节 | 等待提供对应章节数据 |

### 2. Notebook 迁移为 `.py`

当前项目中暂未发现 `.ipynb` 文件，因此尚未生成 Notebook 对应的 `.py` 文件。

待处理：

| 课程 | 原文件 | 输出文件 | 状态 |
| --- | --- | --- | --- |
| 商业数据分析 | `.ipynb` | `.py` | 等待提供 |

### 3. 上传到开源仓库

当前已上传到 GitHub：

```text
https://github.com/fengjunda888/data-analysis-visualization-course
```

Gitee 暂未配置；如需同步，需要提供 Gitee 仓库地址或账号信息。

## 二、已完成图表清单

`reproduce_chapter2_charts.py` 共复现 30 个图表案例：

1. 渐变柱形图
2. 带均值柱形图
3. 渐变圆角柱形图
4. 标注柱形图
5. 层叠柱形图
6. 蝴蝶图
7. 蝴蝶图（百分比）
8. 数值百分比
9. 对比柱形图
10. 甘特图
11. 平滑折线图
12. 菱形走势图
13. 对比折线图
14. 单值圆环图
15. 水球图
16. 波浪水球图
17. 玉玦图
18. 跑道图
19. 南丁格尔圆饼图
20. 南丁格尔圆环图
21. 南丁格尔图（PPT版）
22. 仪表盘图
23. 柱形折线图
24. 目标柱形图
25. 子弹图
26. 柱形圆
27. 簇状柱形折线图
28. 复合柱形图
29. 滑珠图
30. 对比滑珠图

## 三、实验理解

本章实验的核心不是学习单一图表语法，而是把 Excel 图表的视觉表达拆解为以下要素：

- 数据来源：每个工作表中的分类字段、数值字段、占位字段或辅助计算字段。
- 表达目的：比较、排序、结构占比、目标达成、时间进度、趋势变化。
- Python 实现：用 `openpyxl` 读取 Excel，用 `matplotlib` 和 `numpy` 构建对应图形。
- 输出结果：将每个案例保存为可复用的 PNG 图片。

这种迁移方式可以让 Excel 中的静态图表转化为可批量运行、可版本管理、可继续扩展的 Python 实验代码。
