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

## 2026 Python 数据科学生态系统

Python 的数据科学生态在 2026 年发生了显著变化。以下是最值得关注的新工具和趋势。

### Polars：Pandas 的现代替代品

Pandas 仍然是 Python 数据处理的标配，但 [Polars](https://pola.rs/) 在 2026 年已经成为一个不可忽视的竞争者：

| 对比维度 | Pandas | Polars |
|----------|--------|--------|
| 执行模型 | 即时执行（Eager） | 惰性执行（Lazy），查询优化器自动优化 |
| 多核利用 | 默认单核，Pandas 2.x 开始改善 | 原生多核并行 |
| 大数据集性能 | 中等规模（<10GB）表现好 | 10GB+ 数据集显著更快，部分场景快 10-50 倍 |
| 内存效率 | 会复制数据，内存占用高 | 零拷贝和查询下推，内存更高效 |
| API 风格 | DataFrame API，多年积累 | 类似 Pandas 但有自己习惯 |
| 流式处理 | 不支持 | 支持流式处理超大文件（内存只保存窗口数据） |

> 来源：Kanaries, "Polars vs Pandas：2026 年你该用哪个 DataFrame 库？", https://docs.kanaries.net/zh/articles/polars-vs-pandas。

**实践建议**：Pandas 对中小规模数据、快速原型和 Jupyter 交互式分析仍然是最顺手的；Polars 在面对大数据集、性能瓶颈和生产流水线时更具优势。很多团队的做法是——Pandas 做探索分析，Polars 做生产管道。

### Jupyter AI：AI 驱动的交互式计算

2025-2026 年，Jupyter 生态最大的变化是 **Jupyter AI** 的成熟。这是 JupyterLab 的官方 AI 扩展，把大语言模型直接带入 notebook 体验：

- **`%%ai` 魔法命令**：在 notebook cell 中用一行命令调用 AI，如 `%%ai chatgpt` 或 `%%ai ollama`，直接把 AI 输出嵌入实验流程。
- **多提供商支持**：支持 OpenAI、Anthropic、Gemini、HuggingFace、Ollama、MistralAI 等主流提供商。
- **Notebook Intelligence (NBI)**：2025 年 3 月推出的扩展，支持 AI 补全、代码生成和工具调用。
- **本地模型支持**：通过 Ollama 和 GPT4All 运行本地模型，适合隐私敏感场景。

> 来源：LLM Info, "Jupyter AI", https://llm.info/tools/jupyter-ai。

### 其他值得关注的工具

| 工具 | 定位 | 说明 |
|------|------|------|
| **DuckDB** | 嵌入式分析数据库 | 直接对 CSV/Parquet 文件运行 SQL，无需导入。适合快速数据探索 |
| **FireDucks** | Pandas 加速替代 | 兼容 Pandas API 但并行化执行，宣称可比 Pandas 快 10x 以上 |
| **PyTorch 2.x / JAX** | 深度学习框架 | PyTorch 2.x 的 `torch.compile` 大幅优化训练性能；JAX 在科研场景中增长迅速 |
| **scikit-learn 2.0+** | 传统 ML 工具包 | 持续更新中，加入更多实用接口 |

> 来源：Daily Dose of Data Science, "FireDucks vs. Pandas vs. DuckDB vs. Polars", https://www.dailydoseofds.com/p/fireducks-vs-pandas-vs-duckdb-vs-polars/。

### 2026 学习路径建议

对于初学者，推荐的学习顺序已经与几年前有所不同：

1. **Python 基础**（变量、控制流、函数）→ 2-3 周
2. **Pandas 基础**（读取 CSV、筛选、分组聚合）→ 1-2 周
3. **NumPy 基础**（数组操作、广播）→ 配合 Pandas 学习
4. **DuckDB 或 Polars**（大数据集处理）→ 有需要时再学
5. **Matplotlib / Seaborn**（可视化）→ 贯穿始终
6. **scikit-learn 快速上手**（训练第一个模型）→ 1 周
7. **Jupyter AI 辅助** → 用于加速实验和理解代码

### 环境管理最佳实践

| 工具 | 用途 | 推荐指数 |
|------|------|----------|
| **uv** | 2025-2026 年新兴的极速包管理工具，替代 pip/poetry | ⭐⭐⭐⭐⭐ |
| **conda / mamba** | 管理复杂依赖和 Python 版本 | ⭐⭐⭐⭐ |
| **venv** | Python 内置虚拟环境，轻量可靠 | ⭐⭐⭐⭐ |
| **Dev Containers** | VSCode 容器开发环境，项目环境完全隔离 | ⭐⭐⭐ |

> 参考：ABC Trainings, "Artificial Intelligence Fundamentals India 2026", https://abctraining.in/blog/artificial-intelligence-fundamentals-india-1775082075095。

## 延伸阅读

- [数据与特征工程](../数据与特征工程/)
- [机器学习基础](../机器学习基础/)
- [PyTorch](/工具专区/PyTorch/)
- [TensorFlow](/工具专区/TensorFlow/)
- [生成式 AI 基础](../生成式AI基础/)

## 资料整理状态

> 自动采集只作为后台资料来源，不直接发布搜索结果链接；教程正文需要经过阅读、筛选、归纳后再更新。

<!-- RESOURCES_START -->

- 后台候选资料：4 条，覆盖 3 个来源域名。
- 最近采集日期：2026-07-02。
- 发布规则：候选资料必须先经过阅读、去重、事实核验和中文归纳，再合并进正文；本区块不发布原始搜索结果。

<!-- RESOURCES_END -->

*资源区块更新时间：2026-07-23 00:09:06*
