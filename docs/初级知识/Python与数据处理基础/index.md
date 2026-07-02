# Python 与数据处理基础

Python 是 AI 学习和工程实践中最常用的语言。初学阶段不需要成为 Python 专家，但要能读写数据、调用库、训练简单模型并理解报错。

## 需要掌握到什么程度

| 能力 | 要求 |
|------|------|
| 基础语法 | 变量、条件判断、循环、函数、列表、字典 |
| 文件处理 | 读取 CSV、JSON、文本文件 |
| 数据处理 | 筛选、排序、缺失值处理、分组统计 |
| 数值计算 | 理解数组、矩阵、广播、维度 |
| 可视化 | 能画折线图、柱状图、散点图 |
| 环境管理 | 会使用虚拟环境和安装依赖 |

## 常用库

| 库 | 用途 | 入门任务 |
|----|------|----------|
| NumPy | 数组和矩阵计算 | 创建数组、矩阵乘法、统计均值 |
| Pandas | 表格数据处理 | 读取 CSV、筛选行列、处理缺失值 |
| Matplotlib | 基础可视化 | 绘制趋势图和分布图 |
| Seaborn | 统计图表 | 快速查看变量关系 |
| scikit-learn | 传统机器学习 | 训练分类和回归模型 |
| Jupyter | 交互式实验 | 边写代码边查看结果 |

## 数据处理基本流程

```text
读取数据 → 查看字段 → 清洗缺失和异常 → 特征转换 → 划分数据集 → 训练模型 → 评估结果
```

初学者要养成先看数据再训练模型的习惯：

- 数据有多少行、多少列？
- 每列是什么意思？
- 是否有缺失值、重复值、异常值？
- 标签是否均衡？
- 训练数据和真实使用场景是否一致？

## 最小代码结构

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("data.csv")

X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(accuracy_score(y_test, pred))
```

这段代码体现了机器学习项目的核心骨架：数据、特征、标签、训练、预测、评估。

## 环境建议

- 本地入门：Python + VS Code + Jupyter。
- 免安装入门：Google Colab、Kaggle Notebook。
- 包管理：优先使用虚拟环境，避免全局环境依赖混乱。
- 项目结构：把数据、代码、模型输出和文档分开。

## 常见错误

| 问题 | 原因 | 处理 |
|------|------|------|
| 路径找不到 | 当前工作目录不对 | 打印当前目录，使用相对路径 |
| 维度不匹配 | 输入特征形状错误 | 查看 `shape` |
| 有缺失值报错 | 模型不接受 NaN | 填充或删除缺失值 |
| 中文乱码 | 编码不一致 | 尝试 `encoding="utf-8"` 或 `gbk` |
| 训练分数很高、测试很低 | 过拟合或数据泄漏 | 重新划分数据，检查特征 |

## 延伸阅读

- [数据与特征工程](../数据与特征工程/)
- [机器学习基础](../机器学习基础/)
- [PyTorch](/工具专区/PyTorch/)
- [TensorFlow](/工具专区/TensorFlow/)

## 精选资源

> 该区块由采集脚本根据资源库自动重建，只保留当前专题最相关的精选链接；正文教程不会被自动覆盖。

<!-- RESOURCES_START -->

- **[使用Python进行数据分析](https://geeksforgeeks.org/data-analysis/data-analysis-with-python)**
  - 来源：`geeksforgeeks.org` · 质量分：11 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - NumPy 数组 存储相同数据类型的元素并支持多个维度。 切片 允许访问数组中的一系列元素。 Pandas 是一个用于处理结构化（关系或标记）数据的 Python 库。 Series 是一个一维标记数组，能够保存任何数据类型（整数、字符串、浮点数等）。 DataFrame 是一种具有行和列的二维标记数据结构，类似于表格或电子表格。 * ****info():**** 显示数据集结构、列名称、数据类型和非空值。 分组和聚合基于列对数据进行...

- **[使用 Python 探索和分析数据 - 培训 |微软学习](https://learn.microsoft.com/en-us/training/modules/explore-analyze-data-with-python)**
  - 来源：`learn.microsoft.com` · 质量分：10 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - 不再支持该浏览器。升级到 Microsoft Edge 以利用最新功能、安全更新和技术支持。 # 使用 Python 探索和分析数据。数据探索和分析是数据科学的核心。数据科学家需要使用 Python 等编程语言的技能来探索、可视化和操作数据。在本模块中，您将学习： * 常见的数据探索和分析任务。 * 如何使用 NumPy、Pandas 和 Matplotlib 等 Python 包来分析数据。 * 有一些 Python 编程经验。 ##...

- **[第 8 章 Pandas 入门 - 交互的Python：数据分析入门](https://shixiangwang.github.io/pybook/08-pandas-intro)**
  - 来源：`shixiangwang.github.io` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - ## 8.1 Pandas 简介¶. ## 8.2 Pandas 的数据结构¶. ### 8.2.1 Series¶. In [1]: import pandas as pd In [2]: import numpy as np In [4]: {'0':0, '1':1, '2': 2} Out[4]: {'0': 0, '1': 1, '2': 2} In [5]: np.arange(3) Out[5]: array([0, 1,...

- **[第 12 章 Pandas 进阶 - 交互的Python：数据分析入门](https://shixiangwang.github.io/pybook/12-advanced-pandas)**
  - 来源：`shixiangwang.github.io` · 质量分：9 · 首次采集：2026-07-02 · 信息源：`tavily` · 已验证：2026-07-02
  - * 12.1 深入研究 Pandas 数据结构。 ### 12.1.1 回顾¶. In [1]: import numpy as np In [2]: a = np.arange(9) In [3]: a Out[3]: array([0, 1, 2, 3, 4, 5, 6, 7, 8]) In [4]: b = np.arange(9).reshape((3, 3)) In [5]: b Out[5]: array([[0, 1, 2...

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-02 11:56:59*
