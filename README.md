# 大数据分析及数据可视化课程实验

本仓库用于整理课程《大数据分析及数据可视化》的实验内容，并将教材中通过 Excel、Power BI 或 Python Notebook 完成的案例迁移为可重复运行的 Python 实验代码。

当前已完成内容为：《Excel数据可视化——从图表到数据大屏》第二章图表案例的 Python 复现。

## 实验目标

1. 对教材中使用 Excel 或 Power BI 完成的案例，先理解业务含义、数据结构和图表表达目标，再迁移为 Python 实现。
2. 对教材中本身以 Python Notebook 实现的案例，将 `.ipynb` 整理为可直接运行的 `.py` 文件，并补充代码含义说明。
3. 将整理后的实验内容上传到个人开源仓库，便于复习、提交作业和持续扩展。

## 当前目录

```text
.
├── README.md
├── requirements.txt
├── reproduce_chapter2_charts.py
├── chapter2_python_charts/
├── docs/
│   └── experiment_catalog.md
├── 第二章 图表(前15).xlsx
├── 第二章 图表(后15).xlsx
└── 《Excel数据可视化——从图表到数据大屏》.pptx
```

## 已完成实验

| 实验 | 来源教材 | 原始实现 | Python 迁移结果 |
| --- | --- | --- | --- |
| 第二章 30 个图表案例 | 《Excel数据可视化——从图表到数据大屏》 | Excel 图表 | `reproduce_chapter2_charts.py` |

输出图片位于：

```text
chapter2_python_charts/
```

## 运行方法

安装依赖：

```powershell
pip install -r requirements.txt
```

重新生成 30 个图表：

```powershell
python reproduce_chapter2_charts.py
```

脚本会读取当前目录下的两个 Excel 工作簿：

- `第二章 图表(前15).xlsx`
- `第二章 图表(后15).xlsx`

并生成 30 张 PNG 图表到 `chapter2_python_charts/`。

## 迁移说明

本实验不是简单截图复刻，而是将 Excel 图表背后的数据表达方式迁移到 Python 中：

- 柱形图、折线图、组合图使用 `matplotlib` 复现。
- 圆环图、水球图、仪表盘图等仪表类图表使用 `matplotlib.patches` 与极坐标图形构造。
- 甘特图、子弹图、滑珠图等管理分析图表使用横向条形图、散点标记和辅助线实现。
- 所有图表数据均从原始 Excel 工作表读取，避免手工硬编码主要数据。

## 待补充

以下内容需要在提供对应教材资料后继续迁移：

- 《商业数据分析》中 Excel 案例的 Python 实验。
- 《商业数据分析》中 Power BI 案例的 Python 实验。
- 《商业数据分析》中 `.ipynb` 文件整理为 `.py` 文件。
- 《Excel数据可视化——从图表到数据大屏》后续章节案例。

## GitHub 仓库

当前 GitHub 仓库：

https://github.com/fengjunda888/data-analysis-visualization-course

