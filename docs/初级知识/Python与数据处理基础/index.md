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

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-04 00:07:49*
